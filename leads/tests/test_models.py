from django.test import TestCase
from django.core.exceptions import ValidationError

from leads.models import Lead
from companies.models import Company

import pytest

@pytest.mark.django_db
class TestLeadModelValidation:

    @pytest.mark.parametrize(
        "first_name, phone_number, product, description, email",
        [
            ("John", "800x340203", Lead.FinancialProducts.LOAN, "Detailed info", "john@example.com"),  # Invalid number
            ("Mary1222", "48884998458", Lead.FinancialProducts.DEPOSITS, "More details", "mary@example.com"), # Invalid first_name
            ("", "678 288 199", Lead.FinancialProducts.CURRENCY, "Info", "invalid@example.com"), # Empty first_name
            ("Tom", "invalid-number", Lead.FinancialProducts.CURRENCY, "Info", "tom@example.com"), # Invalid number
            ("Jane", "", Lead.FinancialProducts.CREDIT_CARD, "Info", "jane@example.com"),  # Empty number 
            ("Alice", "1234567890", "Product", "Info", ""),  # Invalid product
            ("Jannet", "56464334550", Lead.FinancialProducts.CREDIT_CARD, "", ""),  # Empty description
            ("Daniel", "985987489", "", "Info", ""),  # Empty product

        ]
    )
    def test_lead_creation_with_invalid_inputs(self, first_name, phone_number, product, description, email):
        lead = Lead(
            first_name=first_name,
            phone_number=phone_number,
            product=product,
            description=description,
            email=email,
        )

        with pytest.raises(ValidationError):
            lead.full_clean() 


    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "agent, team",
        [
            ("test_support_agent", "test_sales_team"),
            ("test_sales_agent", "test_support_team"),
        ]
    )
    def test_lead_creation_with_various_agents_and_teams(self, request, agent, team):
        lead = Lead(
            first_name="Tom",
            phone_number="985987849",
            product=Lead.FinancialProducts.CREDIT_CARD,
            description="Info",
            team=request.getfixturevalue(team),
            agent=request.getfixturevalue(agent),
        )

        with pytest.raises(ValidationError):
            lead.full_clean()


class TestLeadModel(TestCase):
    
    @pytest.fixture(autouse=True)
    def setup_with_company(self, test_company):
        self.company = test_company

        self.lead, _ = Lead.objects.get_or_create(
            first_name="Tom",
            phone_number="985987849",
            product=Lead.FinancialProducts.CREDIT_CARD,
        )

    def test_lead_company_assign(self):
        self.assertIsInstance(self.lead.company, Company)
        self.assertEqual("Test", self.lead.company.name)

    def test_str_method_display(self):
        self.assertEqual(str(self.lead), "Tom: 985987849")
