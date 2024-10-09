"""Тест маршрутов."""

from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

ADMIN = lazy_fixture('admin_client')
AUTHOR = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')
HOME_URL = lazy_fixture('url_news_home')
LOGIN_URL = lazy_fixture('url_user_login')
LOGOUT_URL = lazy_fixture('url_user_logout')
SIGNUP_URL = lazy_fixture('url_user_signup')
DETAIL_URL = lazy_fixture('url_news_detail')
EDIT_URL = lazy_fixture('url_comment_edit')
DELETE_URL = lazy_fixture('url_comment_delete')
REDIRECT_DETAIL = lazy_fixture('redirect_detail')
REDIRECT_DELETE = lazy_fixture('redirect_delete')
REDIRECT_EDIT = lazy_fixture('redirect_edit')

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (HOME_URL, CLIENT, HTTPStatus.OK),
        (DETAIL_URL, CLIENT, HTTPStatus.OK),
        (LOGIN_URL, CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, CLIENT, HTTPStatus.OK),
        (EDIT_URL, AUTHOR, HTTPStatus.OK),
        (DELETE_URL, AUTHOR, HTTPStatus.OK),
        (EDIT_URL, ADMIN, HTTPStatus.NOT_FOUND),
        (DELETE_URL, ADMIN, HTTPStatus.NOT_FOUND),
        (DELETE_URL, CLIENT, HTTPStatus.FOUND),
        (EDIT_URL, CLIENT, HTTPStatus.FOUND)

    ),
)
def test_pages_availability_for_anonymous_user(
    url, parametrized_client, expected_status, comment
):
    """Проверка доступа к страницам."""
    assert parametrized_client.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect',
    (
        (DELETE_URL, REDIRECT_DELETE),
        (EDIT_URL, REDIRECT_EDIT)
    )
)
def test_redirect_for_anonymous_client(
    client,
    comment,
    url,
    redirect
):
    """Проверка редиректа для анонимного пользователя."""
    assertRedirects(client.get(url), redirect)
