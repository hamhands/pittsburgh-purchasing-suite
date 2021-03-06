# -*- coding: utf-8 -*-

import re

from flask_wtf import FlaskForm
from wtforms.fields import TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from purchasing.users.models import Department
from flask_security.forms import RegisterForm
from purchasing.public.models import AcceptedEmailDomains
from purchasing.users.models import Role

DOMAINS = re.compile('@[\w.]+')

class DepartmentForm(FlaskForm):
    '''Allows user to update profile information

    Attributes:
        department: sets user department based on choice of available
            departments or none value
        first_name: sets first_name value based on user input
        last_name: sets last_name value based on user input
    '''
    department = QuerySelectField(
        query_factory=Department.query_factory,
        get_pk=lambda i: i.id,
        get_label=lambda i: i.name,
        allow_blank=True, blank_text='-----'
    )
    first_name = TextField()
    last_name = TextField()

class ExtendedRegisterForm(RegisterForm):
    '''Custom registration form to enforce accepted emails

    Attributes:
        pass
    '''
    roles = QuerySelectMultipleField(
        query_factory=Role.staff_factory,
        get_pk=lambda i: i.id,
        get_label=lambda i: i.name
    )

    def __init__(self, *args, **kwargs):
        super(ExtendedRegisterForm, self).__init__(*args, **kwargs)
        if not self.roles.data:
            self.roles.data = [Role.query.filter(Role.name == 'staff').first()]

    def validate(self):
        if not super(ExtendedRegisterForm, self).validate():
            return False

        domain = re.search(DOMAINS, self.email.data)
        domain_text = domain.group().lstrip('@')
        if not all([domain, AcceptedEmailDomains.valid_domain(domain_text)]):
            self.email.errors.append(
                "That's not a valid email domain! You must be associated with the city."
            )
            return False
        return True
