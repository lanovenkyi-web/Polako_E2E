from playwright.sync_api import expect
from BugBusters.utils.common_actions import close_whats_new_popup

from BugBusters.pages.profile_page import ProfilePage
from BugBusters.utils.common_actions import reload_profile_page
from BugBusters.data.constants import Constants


def test_successfully_update_first_name(authorized_page):
    profile_page = ProfilePage(authorized_page)

    old_first_name = profile_page.get_first_name_value()
    new_first_name = "Kate"

    try:
        profile_page.update_name(new_first_name)

        profile_page = reload_profile_page(authorized_page)

        expect(profile_page.first_name).to_have_value(new_first_name)

    finally:
        profile_page = ProfilePage(authorized_page)
        profile_page.update_name(old_first_name)
        reload_profile_page(authorized_page)


def test_failed_update_first_name(authorized_page):
    profile_page = ProfilePage(authorized_page)

    old_first_name = profile_page.get_first_name_value()
    valid_first_name = "Kate"
    invalid_first_name = ""

    try:
        profile_page.update_name(valid_first_name)

        profile_page = reload_profile_page(authorized_page)

        expect(profile_page.first_name).to_have_value(valid_first_name)

        profile_page.update_name(invalid_first_name)

        profile_page = reload_profile_page(authorized_page)

        expect(profile_page.first_name).to_have_value(valid_first_name)

    finally:
        profile_page = ProfilePage(authorized_page)
        profile_page.update_name(old_first_name)
        reload_profile_page(authorized_page)



