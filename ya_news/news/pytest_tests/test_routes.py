"""Тест маршрутов."""

from http import HTTPStatus
from collections import namedtuple

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

PK = 1
ADMIN = lazy_fixture('admin_client')
AUTHOR = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')

URL_NAME = namedtuple(
    'URL_NAME',
    [
        'home',
        'detail',
        'edit',
        'delete',
        'login',
        'logout',
        'signup',
    ],
)

URL = URL_NAME(
    reverse('news:home'),
    reverse('news:detail', args=(PK,)),
    reverse('news:edit', args=(PK,)),
    reverse('news:delete', args=(PK,)),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (URL.home, CLIENT, HTTPStatus.OK),
        (URL.detail, CLIENT, HTTPStatus.OK),
        (URL.login, CLIENT, HTTPStatus.OK),
        (URL.logout, CLIENT, HTTPStatus.OK),
        (URL.signup, CLIENT, HTTPStatus.OK),
        (URL.edit, AUTHOR, HTTPStatus.OK),
        (URL.delete, AUTHOR, HTTPStatus.OK),
        (URL.edit, ADMIN, HTTPStatus.NOT_FOUND),
        (URL.delete, ADMIN, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_availability_for_anonymous_user(
    url, parametrized_client, expected_status, comment
):
    """Проверка доступа к страницам."""
    assert parametrized_client.get(url).status_code == expected_status


@pytest.mark.parametrize('url', (URL.edit, URL.delete))
def test_redirect_for_anonymous_client(client, url, comment, redirect_login):
    """Проверка редиректа для анонимного пользователя."""
    expected_url = redirect_login + url
    assertRedirects(client.get(url), expected_url)
