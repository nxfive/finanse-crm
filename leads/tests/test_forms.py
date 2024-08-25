from leads.forms import LeadBaseForm
from leads.models import Lead

import pytest


@pytest.mark.django_db
class TestLeadBaseFormValidation:

    @pytest.mark.parametrize(
        "first_name, phone_number, product, description, email, team, agent",
        [
            ("John", "800x340203", Lead.FinancialProducts.LOAN, "Detailed info", "john@example.com", None, None),  # Invalid number
            ("Mary1222", "48884998458", Lead.FinancialProducts.DEPOSITS, "More details", "mary@example.com", None, None), # Invalid first_name
            ("", "678 288 199", Lead.FinancialProducts.CURRENCY, "Info", "invalid@example.com", None, None), # Empty first_name
            ("Tom", "invalid-number", Lead.FinancialProducts.CURRENCY, "Info", "tom@example.com", None, None), # Invalid number
            ("Jane", "", Lead.FinancialProducts.CREDIT_CARD, "Info", "jane@example.com", None, None),  # Empty number 
            ("Alice", "1234567890", "Product", "Info", "", None, None),  # Invalid product
            ("Jannet", "56464334550", Lead.FinancialProducts.CREDIT_CARD, "", "", None, None),  # Empty description
            ("Daniel", "985987489", "", "Info", "", None, None),  # Empty product
            ("Mary", "987656798", Lead.FinancialProducts.LOAN, "Info", "", None, "test_sales_agent"), # Sales Team not defined
            ("Jerry", "985446798", Lead.FinancialProducts.LOAN, "Info", "", None, "test_support_agent"), # Support Team not defined
            ("Jenny", "985987485", Lead.FinancialProducts.CREDIT_CARD, "Info", "", "test_sales_team", "test_support_agent"), # Team Type != Agent Role
            ("Russel", "989854185", Lead.FinancialProducts.CREDIT_CARD, "Info", "", "test_support_team", "test_sales_agent"), # Team Type != Agent Role
            ("Russel", "889854185", Lead.FinancialProducts.CREDIT_CARD, "Info", "", "test_support_team", "test_support_agent"), # Team Type != Agent Role

        ]
    )
    def test_form_with_invalid_inputs(self, request, first_name, phone_number, product, description, email, team, agent):

        map = {
            Lead.FinancialProducts.NONE: "Select Product",
            Lead.FinancialProducts.CREDIT_CARD: "Credit Card",
            Lead.FinancialProducts.INVESTMENTS: "Investments",
            Lead.FinancialProducts.DEPOSITS: "Deposits",
            Lead.FinancialProducts.CURRENCY: "Currency",
            Lead.FinancialProducts.LOAN: "Loan",
            "Product": "Product"
        }

        form_data = {
            "first_name": first_name,
            "phone_number": phone_number,
            "product": map[product],
            "description": description,
            "email": email,
            "team": request.getfixturevalue(team) if team else None,
            "agent": request.getfixturevalue(agent) if agent else None,
        }
        form = LeadBaseForm(data=form_data)
        assert not form.is_valid()
