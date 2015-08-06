# -*- coding: utf-8 -*-

import re
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import (
    TextField, IntegerField, DateField, TextAreaField, HiddenField
)
from wtforms.validators import DataRequired, URL, Optional, ValidationError

EMAIL_REGEX = re.compile(r'^.+@([^.@][^@]+)$', re.IGNORECASE)

def not_all_hidden(form, field):
    '''Makes sure that every field isn't blank
    '''
    if not any([v for (k, v) in form.data.items() if k != field.name]):
        raise ValidationError('You must update at least one field!')

def validate_multiple_emails(form, field):
    '''Parses a semicolon-delimited list of emails, validating each
    '''
    if field.data:
        for email in field.data.split(';'):
            if not re.match(EMAIL_REGEX, email):
                raise ValidationError('One of the supplied emails is invalid!')

class EditContractForm(Form):
    '''Form to control details needed to finalize a new/renewed contract
    '''

    description = TextField(validators=[DataRequired()])
    financial_id = IntegerField(validators=[DataRequired(message="A number is required.")])
    expiration_date = DateField(validators=[DataRequired()])
    spec_number = TextField(validators=[DataRequired()])
    contract_href = TextField(validators=[Optional(), URL(message="That URL doesn't work!")])

class ContractMetadataForm(Form):
    '''Edit a contract's metadata during the renewal process
    '''
    financial_id = IntegerField(validators=[Optional()])
    expiration_date = DateField(validators=[Optional()])
    spec_number = TextField(validators=[Optional()], filters=[lambda x: x or None])
    all_blank = HiddenField(validators=[not_all_hidden])

class SendUpdateForm(Form):
    '''Form to update
    '''
    send_to = TextField(validators=[DataRequired(), validate_multiple_emails])
    send_to_cc = TextField(validators=[Optional(), validate_multiple_emails])
    subject = TextField(validators=[DataRequired()])
    body = TextAreaField(validators=[DataRequired()])

class PostOpportunityForm(Form):
    '''
    '''
    pass

class NoteForm(Form):
    '''Adds a note to the contract stage view
    '''
    note = TextAreaField(validators=[DataRequired(message='Note cannot be blank.')])

class FileUploadForm(Form):
    upload = FileField('datafile', validators=[
        FileAllowed(['csv'], message='.csv files only')
    ])

class ContractUploadForm(Form):
    contract_id = HiddenField('id', validators=[DataRequired()])
    upload = FileField('datafile', validators=[
        FileAllowed(['pdf'], message='.pdf files only')
    ])
