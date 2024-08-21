from django import template

register = template.Library()


def join_companies(companies):
    return ", ".join(str(company) for company in companies)


register.filter("join_companies", join_companies)
