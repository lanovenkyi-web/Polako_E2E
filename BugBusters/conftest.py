import os
import time
import uuid
import pytest

from playwright.sync_api import Page
from dotenv import load_dotenv

from BugBusters.app import App
from BugBusters.data.constants import Constants
from BugBusters.utils.popups import close_whats_new_popup

load_dotenv(
    dotenv_path=os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".env"
    )
)


@pytest.fixture
def app(page: Page):
    page.goto(Constants.BASE_URL, wait_until="domcontentloaded")
    yield App(page)


@pytest.fixture
def base_user_data():
    return {
        "name": Constants.USER_NAME,
        "password": Constants.PASSWORD,
    }


@pytest.fixture
def new_user_data(base_user_data):
    return {
        **base_user_data,
        "email": f"qa_user_{uuid.uuid4().hex[:5]}@gmail.com",
    }


@pytest.fixture
def existing_user_data(base_user_data):
    return {
        **base_user_data,
        "email": Constants.EMAIL,
    }


@pytest.fixture
def login_user_data():
    assert Constants.EMAIL, "EMAIL не найден в .env"
    assert Constants.PASSWORD, "PASSWORD не найден в .env"

    return {
        "email": Constants.EMAIL,
        "password": Constants.PASSWORD,
    }

@pytest.fixture
def authorized_page(browser, login_user_data):
    context = browser.new_context(
        base_url=Constants.SITE_URL,
        extra_http_headers={
            "Origin": Constants.SITE_URL,
            "Referer": Constants.BASE_URL,
        }
    )

    context.set_default_navigation_timeout(60000)

    login_response = context.request.post(
        "/api/auth/login",
        data={
            "email": login_user_data["email"],
            "password": login_user_data["password"],
            "mode": "cookie",
        }
    )

    assert login_response.ok, (
        f"Login failed: {login_response.status} {login_response.text()}"
    )

    login_data = login_response.json()
    access_token = login_data["data"]["access_token"]

    context.add_cookies([
        {
            "name": "access_token",
            "value": access_token,
            "domain": "stg.polakohedonist.club",
            "path": "/",
            "expires": int(time.time()) + 20 * 60,
            "httpOnly": False,
            "secure": True,
            "sameSite": "Lax",
        }
    ])

    page = context.new_page()

    page.goto(
        f"{Constants.BASE_URL}/user/personal-information",
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_load_state("networkidle", timeout=15000)

    close_whats_new_popup(page)

    assert "/user/personal-information" in page.url, (
        f"User is not authorized. Current URL: {page.url}"
    )

    page.locator('input[name="email"]').wait_for(
        state="visible",
        timeout=15000
    )

    yield page

    context.close()
