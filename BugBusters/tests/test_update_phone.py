from playwright.sync_api import expect

from BugBusters.pages.profile_page import ProfilePage
from BugBusters.utils.common_actions import reload_profile_page


def test_successfully_update_phone(authorized_page):
    profile_page = ProfilePage(authorized_page)

    old_phone = profile_page.get_phone_value()
    new_phone = "+381601234567"

    try:
        profile_page.update_phone(new_phone)

        profile_page = reload_profile_page(authorized_page)

        expect(profile_page.phone).to_have_value(new_phone)

    finally:
        profile_page = reload_profile_page(authorized_page)
        profile_page.update_phone(old_phone)
        reload_profile_page(authorized_page)