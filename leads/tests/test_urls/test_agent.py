from django.test import Client
from django.urls import reverse

import pytest


@pytest.mark.usefixtures("test_support_agent", "test_support_team", "test_sales_team", "test_lead_support", "test_lead_support_agent", "test_lead_sales")
@pytest.mark.django_db
class TestLeadUrlsForAgent:
    """
        Test all urls from leads app for agent user.

        This test class ensures that URL patterns related to leads are accessible 
        and correctly handled for users with agent permissions.

        Attributes:
            test_lead_support (Lead): A lead assigned only to the agent's team.
            test_lead_support_agent (Lead): A lead assigned to the agent's team 
                and specifically to the agent.
            test_lead_sales (Lead): A lead not assigned to the agent's team. 
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_support_agent):
        self.client = Client()
        self.client.login(username=test_support_agent.user.email, password="Password12345")

# /leads/
    def test_lead_list_url(self, test_support_agent):
        response = self.client.get(reverse("leads:lead-list"))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    def test_lead_create_url(self, test_support_agent):
        response = self.client.get(reverse("leads:lead-create"))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    # agent's leads
    def test_lead_update_url_own_lead(self, test_support_agent, test_lead_support_agent):
        response = self.client.get(reverse("leads:lead-update", kwargs={"pk": test_lead_support_agent.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    def test_lead_detail_url_own_lead(self, test_support_agent, test_lead_support_agent):
        response = self.client.get(reverse("leads:lead-detail", kwargs={"pk": test_lead_support_agent.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"
    
    def test_lead_delete_url_own_lead(self, test_support_agent, test_lead_support_agent):
        response = self.client.get(reverse("leads:lead-delete", kwargs={"pk": test_lead_support_agent.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

# /<slug:team_slug>/ -- own team
    def test_lead_list_url_with_team_slug(self, test_support_team):
        response = self.client.get(reverse("teams:leads:lead-list",  kwargs={"team_slug": test_support_team.slug}))
        assert response.status_code == 200

    def test_lead_create_url_with_team_slug(self, test_support_team):
        response = self.client.get(reverse("teams:leads:lead-create", kwargs={"team_slug": test_support_team.slug}))
        assert response.status_code == 403

    # leads not assigned to agent
    def test_lead_update_url_with_team_slug_not_own_lead(self, test_support_team, test_lead_support):
        response = self.client.get(reverse("teams:leads:lead-update", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support.pk}))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"

    def test_lead_detail_url_with_team_slug_not_own_lead(self, test_support_team, test_lead_support):
        response = self.client.get(reverse("teams:leads:lead-detail", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support.pk}))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"
    
    def test_lead_delete_url_with_team_slug_not_own_lead(self, test_support_team, test_lead_support):
        response = self.client.get(reverse("teams:leads:lead-delete", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support.pk}))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"

    # leads assigned to agent
    def test_lead_update_url_with_team_slug_own_lead(self, test_support_team, test_lead_support_agent):
        response = self.client.get(reverse("teams:leads:lead-update", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support_agent.pk}))
        assert response.status_code == 200

    def test_lead_detail_url_with_team_slug_own_lead(self, test_support_team, test_lead_support_agent):
        response = self.client.get(reverse("teams:leads:lead-detail", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support_agent.pk}))
        assert response.status_code == 200
    
    def test_lead_delete_url_with_team_slug_own_lead(self, test_support_team, test_lead_support_agent):
        response = self.client.get(reverse("teams:leads:lead-delete", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support_agent.pk}))
        assert response.status_code == 200

# /<slug:team_slug>/ -- not own team

    def test_lead_list_url_with_wrong_team_slug(self, test_support_agent, test_sales_team):
        response = self.client.get(reverse("teams:leads:lead-list",  kwargs={"team_slug": test_sales_team.slug}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    def test_lead_create_url_with_wrong_team_slug(self, test_support_agent, test_sales_team):
        response = self.client.get(reverse("teams:leads:lead-create", kwargs={"team_slug": test_sales_team.slug}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    # leads from other's team
    def test_lead_update_url_with_wrong_team_slug(self, test_support_agent, test_sales_team, test_lead_sales):
        response = self.client.get(reverse("teams:leads:lead-update", kwargs={"team_slug": test_sales_team.slug, "pk": test_lead_sales.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    def test_lead_detail_url_with_wrong_team_slug(self, test_support_agent, test_sales_team, test_lead_sales):
        response = self.client.get(reverse("teams:leads:lead-detail", kwargs={"team_slug": test_sales_team.slug, "pk": test_lead_sales.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"
    
    def test_lead_delete_url_with_wrong_team_slug(self, test_support_agent, test_sales_team, test_lead_sales):
        response = self.client.get(reverse("teams:leads:lead-delete", kwargs={"team_slug": test_sales_team.slug, "pk": test_lead_sales.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"


# /leads/my-leads/
    def test_lead_list_url_my_leads(self, test_support_agent):
        response = self.client.get("/leads/my-leads/")
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    def test_lead_create_url_my_leads(self):
        response = self.client.get("/leads/my-leads/create/")
        assert response.status_code == 404

    # agents's own leads
    def test_lead_update_url_my_leads_own_lead(self, test_support_agent, test_lead_support_agent):
        response = self.client.get(reverse("leads:my-lead-update", kwargs={"pk": test_lead_support_agent.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    def test_lead_detail_url_my_leads_own_lead(self, test_support_agent, test_lead_support_agent):
        response = self.client.get(reverse("leads:my-lead-detail", kwargs={"pk": test_lead_support_agent.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"
    
    def test_lead_delete_url_my_leads_own_lead(self, test_support_agent, test_lead_support_agent):
        response = self.client.get(reverse("leads:my-lead-delete", kwargs={"pk": test_lead_support_agent.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

# /<slug:team_slug>/my-leads/  -- own team
    def test_lead_list_url_with_team_slug_my_leads(self, test_support_team):
        response = self.client.get(reverse("teams:leads:my-lead-list"))
        assert response.status_code == 200
        assert response.url == f"/teams/{test_support_team.slug}/leads/my-leads/"

    def test_lead_create_url_with_team_slug_my_leads(self, test_support_team):
        response = self.client.get(f"/teams/{test_support_team.slug}/leads/my-leads/create/")
        assert response.status_code == 404

    # update/detail/delete lead assigned to agent
    def test_own_lead_update_url_with_team_slug_my_leads(self, test_support_team, test_lead_support_agent):
        response = self.client.get(reverse("teams:leads:my-lead-update", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support_agent.pk}))
        assert response.status_code == 200
      
    def test_own_lead_detail_url_with_team_slug_my_leads(self, test_support_team, test_lead_support_agent):
        response = self.client.get(reverse("teams:leads:my-lead-detail", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support_agent.pk}))
        assert response.status_code == 200
    
    def test_own_lead_delete_url_with_team_slug_my_leads(self, test_support_team, test_lead_support_agent):
        response = self.client.get(reverse("teams:leads:my-lead-delete", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support_agent.pk}))
        assert response.status_code == 200

    # update/detail/delete lead not assigned to agent (only to the agent's team)
    def test_lead_update_url_with_team_slug_my_leads_not_own_lead(self, test_support_team, test_lead_support):
        response = self.client.get(reverse("teams:leads:my-lead-update", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support.pk}))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"

    def test_lead_detail_url_with_team_slug_my_leads_not_own_lead(self, test_support_team, test_lead_support):
        response = self.client.get(reverse("teams:leads:my-lead-detail", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support.pk}))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"

    def test_lead_delete_url_with_team_slug_my_leads_not_own_lead(self, test_support_team, test_lead_support):
        response = self.client.get(reverse("teams:leads:my-lead-delete", kwargs={"team_slug": test_support_team.slug, "pk": test_lead_support.pk}))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"


# /<slug:team_slug>/my-leads/  -- not own team
    def test_lead_list_url_with_wrong_team_slug_my_leads(self, test_support_agent):
        response = self.client.get(reverse("teams:leads:my-lead-list"))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    def test_lead_create_url_with_wrong_team_slug_my_leads(self, test_sales_team):
        response = self.client.get(f"teams/{test_sales_team.slug}/leads/my-leads/create/")
        assert response.status_code == 404

    # not agent's team but agents leads
    def test_lead_update_url_with_wrong_team_slug_my_leads(self, test_support_agent, test_sales_team, test_lead_support_agent):
        response = self.client.get(reverse("teams:leads:my-lead-update", kwargs={"team_slug": test_sales_team.slug, "pk": test_lead_support_agent.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"

    def test_lead_detail_url_with_wrong_team_slug_my_leads(self, test_support_agent, test_sales_team, test_lead_support_agent):
        response = self.client.get(reverse("teams:leads:my-lead-detail", kwargs={"team_slug": test_sales_team.slug, "pk": test_lead_support_agent.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"
    
    def test_lead_delete_url_with_wrong_team_slug_my_leads(self, test_support_agent, test_sales_team, test_lead_support_agent):
        response = self.client.get(reverse("teams:leads:my-lead-delete", kwargs={"team_slug": test_sales_team.slug, "pk": test_lead_support_agent.pk}))
        assert response.status_code == 302
        assert response.url == f"/accounts/dashboard/{test_support_agent.user.username}/"
