from factory.django import DjangoModelFactory
import factory.django
import factory.fuzzy
from accounts.models import Account
from leads.models import Lead
from teams.models import Team
from managers.models import Manager
from accounts.models import Account
from agents.models import Agent
from companies.models import Company


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = "Test"
    slug= "test"
    path = "/test/"
    website = "https://test.com"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = Account

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    phone_number = factory.Faker("phone_number")
    birth_date = factory.Faker("date_of_birth")

    is_active = True
    

class ManagerFactory(DjangoModelFactory):
    class Meta:
        model = Manager
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def set_user_as_manager(self, create, extracted, **kwargs):
        if create:
            self.user.is_manager = True
            self.user.save()

class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Faker("city")
    team_type = Team.TeamTypes.SUPPORT
    manager = factory.SubFactory(ManagerFactory)
    

class AgentFactory(DjangoModelFactory):
    class Meta:
        model = Agent
    user = factory.SubFactory(UserFactory)
    role = Agent.Roles.SUPPORT
    team = factory.SubFactory(TeamFactory)


class LeadFactory(DjangoModelFactory):
    class Meta:
        model = Lead

    first_name = factory.Faker("first_name")
    phone_number = factory.Faker("phone_number")
    product = Lead.FinancialProducts.LOAN
    agent = factory.SubFactory(AgentFactory)
    team = factory.SubFactory(TeamFactory)
    company = factory.SubFactory(Company)
