# -*- coding: utf-8 -*-

import datetime

import factory
from factory.alchemy import SQLAlchemyModelFactory

from purchasing.database import db
from purchasing.users.models import User, Role, Department

from purchasing.data.contracts import ContractBase, ContractProperty, ContractType
from purchasing.data.companies import Company
from purchasing.data.flows import Flow
from purchasing.data.stages import Stage
from purchasing.data.contract_stages import ContractStageActionItem, ContractStage
from purchasing.public.models import AcceptedEmailDomains

from purchasing.opportunities.models import (
    Opportunity, RequiredBidDocument, OpportunityDocument, Category,
    Vendor
)
from purchasing.jobs.job_base import JobStatus

class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session

class RoleFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: '{}'.format(n))

    class Meta:
        model = Role

class DepartmentFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: 'department{}'.format(n))

    class Meta:
        model = Department

class UserFactory(BaseFactory):
    id = factory.Sequence(lambda n: n + 100)
    email = factory.Sequence(lambda n: '{}@foo.com'.format(n))
    created_at = factory.Sequence(lambda n: datetime.datetime.now())
    first_name = factory.Sequence(lambda n: '{}'.format(n))
    last_name = factory.Sequence(lambda n: '{}'.format(n))
    department = factory.SubFactory(DepartmentFactory)
    active = factory.Sequence(lambda n: True)
    confirmed_at = factory.Sequence(lambda n: datetime.datetime.now())

    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        if extracted:
            for role in extracted:
                self.roles.append(role)

    class Meta:
        model = User

class FlowFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    flow_name = factory.Sequence(lambda n: '{}'.format(n))
    stage_order = factory.Sequence(lambda n: n)

    class Meta:
        model = Flow

class StageFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: '{}'.format(n))
    post_opportunities = factory.Sequence(lambda n: n)

    class Meta:
        model = Stage

class CompanyFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)

    class Meta:
        model = Company

class ContractTypeFactory(BaseFactory):
    id = factory.Sequence(lambda n: n + 100)

    class Meta:
        model = ContractType

class ContractStageFactory(BaseFactory):
    id = factory.Sequence(lambda n: 10 + n)
    stage = factory.SubFactory(StageFactory)
    flow = factory.SubFactory(FlowFactory)

    class Meta:
        model = ContractStage

class ContractBaseFactory(BaseFactory):
    id = factory.Sequence(lambda n: 100 + n)
    contract_type = factory.SubFactory(ContractTypeFactory)

    class Meta:
        model = ContractBase

class ContractPropertyFactory(BaseFactory):
    id = factory.Sequence(lambda n: n + 10)
    contract = factory.SubFactory(ContractBaseFactory)

    class Meta:
        model = ContractProperty

class ContractStageActionItemFactory(BaseFactory):
    id = factory.Sequence(lambda n: n + 10)
    contract_stage = factory.SubFactory(ContractStageFactory)

    class Meta:
        model = ContractStageActionItem

class CategoryFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    category_friendly_name = 'i am friendly!'

    class Meta:
        model = Category

class OpportunityFactory(BaseFactory):
    id = factory.Sequence(lambda n: n + 100)
    department = factory.SubFactory(DepartmentFactory)
    contact = factory.SubFactory(UserFactory)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Opportunity

class VendorFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: '{}@foo.com'.format(n))
    business_name = factory.Sequence(lambda n: '{}'.format(n))

    class Meta:
        model = Vendor

class RequiredBidDocumentFactory(BaseFactory):
    class Meta:
        model = RequiredBidDocument

class OpportunityDocumentFactory(BaseFactory):
    class Meta:
        model = OpportunityDocument

class JobStatusFactory(BaseFactory):
    class Meta:
        model = JobStatus

class AcceptedEmailDomainsFactory(BaseFactory):
    class Meta:
        model = AcceptedEmailDomains
