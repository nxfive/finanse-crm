import pytest
from django.contrib.auth.hashers import make_password
from companies.models import Company
from accounts.models import Account
from teams.models import Manager, Team
from agents.models import Agent


@pytest.fixture
def test_admin():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "admin",
        "email": "admin@mail.com",
        "password": make_password("Password12345")
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
        "password": make_password("Password12345")
    }
    user1 = Account.objects.create_user(**data)
    return user1

@pytest.fixture
def test_user2():
    data = {
        "first_name": "Kate",
        "last_name": "Johns",
        "username": "katejohns",
        "email": "katejohns@mail.com",
        "birth_date": "1991-08-21",
        "password": make_password("Password12345")
    }
    user2 = Account.objects.create_user(**data)
    return user2


@pytest.fixture
def test_user3():
    data = {
        "first_name": "Frank",
        "last_name": "Parker",
        "username": "frankparker",
        "email": "frankparker@mail.com",
        "birth_date": "1984-02-13",
        "password": make_password("Password12345")
    }
    user3 = Account.objects.create_user(**data)
    return user3

@pytest.fixture
def test_user4():
    data = {
        "first_name": "Camile",
        "last_name": "Hans",
        "username": "camilehans",
        "email": "camilehans@mail.com",
        "birth_date": "1979-04-05",
        "password": make_password("Password12345")
    }
    user4 = Account.objects.create_user(**data)
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
def test_support_team(test_user1, test_company):
    manager = Manager.objects.create(user=test_user1)
    data = {
        "name": "Los Angeles",
        "manager": manager,
        "team_type": Team.TeamTypes.SUPPORT,
    }
    support_team = Team.objects.create(**data)
    support_team.companies.add(test_company)
    return support_team


@pytest.fixture
def test_sales_team(test_user2, test_company):
    manager = Manager.objects.create(user=test_user2)
    data = {
        "name": "Houston",
        "manager": manager,
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
