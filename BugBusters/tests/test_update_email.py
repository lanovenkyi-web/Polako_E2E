from playwright.sync_api import expect

from BugBusters.pages.profile_page import ProfilePage
from BugBusters.data.constants import Constants


def test_email_is_displayed_correctly(authorized_page):
    profile_page = ProfilePage(authorized_page)

    expect(profile_page.email).to_be_visible()
    expect(profile_page.email).to_have_value(Constants.EMAIL)


def test_email_field_accepts_new_value(authorized_page):
    profile_page = ProfilePage(authorized_page)

    new_email = "test_email@example.com"

    profile_page.email.fill(new_email)

    expect(profile_page.email).to_have_value(new_email)