import pytest
from companies.models import Company
from accounts.models import Account
from teams.models import Manager, Team
from agents.models import Agent
from leads.models import Lead


@pytest.fixture
def test_admin():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "admin",
        "email": "admin@mail.com",
        "password": "Password12345",
    }
    admin = Account.objects.create_superuser(**data)
    return admin


@pytest.fixture
def test_user1():
    data = {
        "first_name": "Kevin",
        "last_name": "Edwards",
        "username": "kevinedwards",
        "email": "kevinedwards@mail.com",
        "birth_date": "1995-10-01",
        "password": "Password12345",
    }
    user1 = Account.objects.create_user(**data)
    user1.is_active=True
    user1.save()
    return user1


@pytest.fixture
def test_user2():
    data = {
        "first_name": "Kate",
        "last_name": "Johns",
        "username": "katejohns",
        "email": "katejohns@mail.com",
        "birth_date": "1991-08-21",
        "password": "Password12345"
    }
    user2 = Account.objects.create_user(**data)
    user2.is_active=True
    user2.save()
    return user2


@pytest.fixture
def test_user3():
    data = {
        "first_name": "Frank",
        "last_name": "Parker",
        "username": "frankparker",
        "email": "frankparker@mail.com",
        "birth_date": "1984-02-13",
        "password": "Password12345"
    }
    user3 = Account.objects.create_user(**data)
    user3.is_active=True
    user3.save()
    return user3


@pytest.fixture
def test_user4():
    data = {
        "first_name": "Camile",
        "last_name": "Hans",
        "username": "camilehans",
        "email": "camilehans@mail.com",
        "birth_date": "1979-04-05",
        "password": "Password12345"
    }
    user4 = Account.objects.create_user(**data)
    user4.is_active=True
    user4.save()
    return user4


@pytest.fixture()
def test_company():
    data = {
        "name": "Test",
        "path": "/test",
        "website": "https://test.com"
    }
    test_company, _ = Company.objects.get_or_create(**data)
    return test_company


@pytest.fixture
def test_manager(test_user1):
    return Manager.objects.create(user=test_user1)


@pytest.fixture
def test_support_team(test_manager, test_company):
    data = {
        "name": "Los Angeles",
        "manager": test_manager,
        "team_type": Team.TeamTypes.SUPPORT,
    }
    support_team = Team.objects.create(**data)
    support_team.companies.add(test_company)
    return support_team


@pytest.fixture
def test_manager2(test_user2):
    return Manager.objects.create(user=test_user2)


@pytest.fixture
def test_sales_team(test_manager2, test_company):
    data = {
        "name": "Houston",
        "manager": test_manager2,
        "team_type": Team.TeamTypes.SALES,
    }
    sales_team = Team.objects.create(**data)
    sales_team.companies.add(test_company)
    return sales_team


@pytest.fixture
def test_support_agent(test_user3, test_support_team, test_company):
    data = {
        "user": test_user3,
        "role": Agent.Roles.SUPPORT,
        "team": test_support_team,
    }
    support_agent = Agent.objects.create(**data)
    support_agent.companies.add(test_company)
    return support_agent


@pytest.fixture
def test_sales_agent(test_user4, test_sales_team, test_company):
    data = {
        "user": test_user4,
        "role": Agent.Roles.SALES,
        "team": test_sales_team,
    }
    sales_team = Agent.objects.create(**data)
    sales_team.companies.add(test_company)
    return sales_team


@pytest.fixture
def test_lead_sales(test_sales_team):
    data = {
        "first_name": "Ann",
        "phone_number": "985987485",
        "product": Lead.FinancialProducts.LOAN,
        "team": test_sales_team,
    }
    lead, _ = Lead.objects.get_or_create(**data)
    return lead


@pytest.fixture
def test_lead_support(test_support_team):
    data = {
        "first_name": "Ann",
        "phone_number": "985987485",
        "product": Lead.FinancialProducts.LOAN,
        "team": test_support_team,
    }
    lead, _ = Lead.objects.get_or_create(**data)
    return lead


@pytest.fixture
def test_lead_support_agent(test_support_team, test_support_agent):
    data = {
        "first_name": "Ann",
        "phone_number": "985987485",
        "product": Lead.FinancialProducts.LOAN,
        "team": test_support_team,
        "agent": test_support_agent,
    }
    lead, _ = Lead.objects.get_or_create(**data)
    return lead
