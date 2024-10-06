"""Тесты маршрутов."""

from http import HTTPStatus

from notes.tests.core import (
    CoreTestCase,
    REVERSE_HOME,
    REVERSE_ADD,
    REVERSE_DELETE,
    REVERSE_DETAIL,
    REVERSE_EDIT,
    REVERSE_LIST,
    REVERSE_LOGIN,
    REVERSE_LOGOUT,
    REVERSE_SIGNUP,
    REVERSE_SUCCESS
)

REDIRECT_LOGIN = f'{REVERSE_LOGIN}?next={{url}}'


class TestRoutes(CoreTestCase):
    """Тестовый класс."""

    def test_pages_availability_for_anonymous_user(self):
        """Проверка доступа к страницам."""
        urls = (
            (REVERSE_HOME, self.client, HTTPStatus.OK),
            (REVERSE_LOGIN, self.client, HTTPStatus.OK),
            (REVERSE_LOGOUT, self.client, HTTPStatus.OK),
            (REVERSE_SIGNUP, self.client, HTTPStatus.OK),
            (REVERSE_DETAIL, self.author_logged, HTTPStatus.OK),
            (REVERSE_EDIT, self.author_logged, HTTPStatus.OK),
            (REVERSE_DELETE, self.author_logged, HTTPStatus.OK),
            (REVERSE_ADD, self.user_logged, HTTPStatus.OK),
            (REVERSE_LIST, self.user_logged, HTTPStatus.OK),
            (REVERSE_SUCCESS, self.user_logged, HTTPStatus.OK),
            (REVERSE_DETAIL, self.user_logged, HTTPStatus.NOT_FOUND),
            (REVERSE_EDIT, self.user_logged, HTTPStatus.NOT_FOUND),
            (REVERSE_DELETE, self.user_logged, HTTPStatus.NOT_FOUND),
        )
        for url, client, expected_status in urls:
            with self.subTest(url=url):
                self.assertEqual(
                    client.get(url).status_code,
                    expected_status,
                )

    def test_redirects(self):
        """Проверка редиректа для неавторизованного пользователя."""
        urls = (
            REVERSE_LIST,
            REVERSE_ADD,
            REVERSE_SUCCESS,
            REVERSE_DETAIL,
            REVERSE_EDIT,
            REVERSE_DELETE,
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    REDIRECT_LOGIN.format(url=url)
                )
