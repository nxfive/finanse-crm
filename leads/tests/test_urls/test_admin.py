from django.test import Client
from django.urls import reverse

import pytest


@pytest.mark.usefixtures("test_admin", "test_support_team", "test_lead")
@pytest.mark.django_db
class TestLeadUrlsForAdmin:
    """
        Test all urls from leads app for admin user.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_admin):
        self.client = Client()
        self.client.login(username=test_admin.email, password="Password12345")

    def test_lead_list_url(self):
        response = self.client.get(reverse("leads:lead-list"))
        assert response.status_code == 200

    def test_lead_create_url(self):
        response = self.client.get(reverse("leads:lead-create"))
        assert response.status_code == 200

    def test_lead_update_url(self, test_lead):
        response = self.client.get(reverse("leads:lead-update", kwargs={"pk": test_lead.pk}))
        assert response.status_code == 200

    def test_lead_detail_url(self, test_lead):
        response = self.client.get(reverse("leads:lead-detail", kwargs={"pk": test_lead.pk}))
        assert response.status_code == 200
    
    def test_lead_delete_url(self, test_lead):
        response = self.client.get(reverse("leads:lead-delete", kwargs={"pk": test_lead.pk}))
        assert response.status_code == 200

# /<slug:team_slug>/
    def test_lead_list_url_with_team_slug(self, test_support_team):
        response = self.client.get(reverse("teams:leads:lead-list",  kwargs={"team_slug": test_support_team.slug}))
        assert response.status_code == 200

    def test_lead_create_url_with_team_slug(self, test_support_team):
        response = self.client.get(reverse("teams:leads:lead-create", kwargs={"team_slug": test_support_team.slug}))
        assert response.status_code == 200

    def test_lead_update_url_with_team_slug(self, test_support_team, test_lead):
        response = self.client.get(reverse("teams:leads:lead-update", kwargs={"team_slug": test_support_team.slug, "pk": test_lead.pk}))
        assert response.status_code == 200

    def test_lead_detail_url_with_team_slug(self, test_support_team, test_lead):
        response = self.client.get(reverse("teams:leads:lead-detail", kwargs={"team_slug": test_support_team.slug, "pk": test_lead.pk}))
        assert response.status_code == 200
    
    def test_lead_delete_url_with_team_slug(self, test_support_team, test_lead):
        response = self.client.get(reverse("teams:leads:lead-delete", kwargs={"team_slug": test_support_team.slug, "pk": test_lead.pk}))
        assert response.status_code == 200

# /leads/my-leads/
    def test_lead_list_url_my_leads(self):
        response = self.client.get("/leads/my-leads/")
        assert response.status_code == 302
        assert response.url == "/leads/"

    def test_lead_create_url_my_leads(self):
        response = self.client.get("/leads/my-leads/create/")
        assert response.status_code == 404

    def test_lead_update_url_my_leads(self, test_lead):
        response = self.client.get(reverse("leads:my-lead-update", kwargs={"pk": test_lead.pk}))
        assert response.status_code == 302
        assert response.url == f"/leads/"

    def test_lead_detail_url_my_leads(self, test_lead):
        response = self.client.get(reverse("leads:my-lead-detail", kwargs={"pk": test_lead.pk}))
        assert response.status_code == 302
        assert response.url == f"/leads/"
    
    def test_lead_delete_url_my_leads(self, test_lead):
        response = self.client.get(reverse("leads:my-lead-delete", kwargs={"pk": test_lead.pk}))
        assert response.status_code == 302
        assert response.url == f"/leads/"

# /<slug:team_slug>/my-leads/
    def test_lead_list_url_with_team_slug_my_leads(self, test_support_team):
        response = self.client.get(reverse("teams:leads:my-lead-list",))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"

    def test_lead_create_url_with_team_slug_my_leads(self, test_support_team):
        response = self.client.get(f"teams/{test_support_team.slug}/leads/my-leads/create/")
        assert response.status_code == 404

    def test_lead_update_url_with_team_slug_my_leads(self, test_support_team, test_lead):
        response = self.client.get(reverse("teams:leads:my-lead-update", kwargs={"team_slug": test_support_team.slug, "pk": test_lead.pk}))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"

    def test_lead_detail_url_with_team_slug_my_leads(self, test_support_team, test_lead):
        response = self.client.get(reverse("teams:leads:my-lead-detail", kwargs={"team_slug": test_support_team.slug, "pk": test_lead.pk}))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"
    
    def test_lead_delete_url_with_team_slug_my_leads(self, test_support_team, test_lead):
        response = self.client.get(reverse("teams:leads:my-lead-delete", kwargs={"team_slug": test_support_team.slug, "pk": test_lead.pk}))
        assert response.status_code == 302
        assert response.url == f"/teams/{test_support_team.slug}/leads/"