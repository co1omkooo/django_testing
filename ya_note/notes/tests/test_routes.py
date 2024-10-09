"""Тесты маршрутов."""

from http import HTTPStatus

from notes.tests.core import (
    CoreTestCase,
    URL_HOME,
    URL_ADD,
    URL_DELETE,
    URL_DETAIL,
    URL_EDIT,
    URL_LIST,
    URL_LOGIN,
    URL_LOGOUT,
    URL_SIGNUP,
    URL_SUCCESS,
    REDIRECT_ADD,
    REDIRECT_DELETE,
    REDIRECT_DETAIL,
    REDIRECT_EDIT,
    REDIRECT_LIST,
    REDIRECT_SUCCESS
)


class TestRoutes(CoreTestCase):
    """Тестовый класс."""

    def test_pages_availability_for_anonymous_user(self):
        """Проверка доступа к страницам."""
        urls = (
            (URL_HOME, self.client, HTTPStatus.OK),
            (URL_LOGIN, self.client, HTTPStatus.OK),
            (URL_LOGOUT, self.client, HTTPStatus.OK),
            (URL_SIGNUP, self.client, HTTPStatus.OK),
            (URL_DETAIL, self.author_logged, HTTPStatus.OK),
            (URL_EDIT, self.author_logged, HTTPStatus.OK),
            (URL_DELETE, self.author_logged, HTTPStatus.OK),
            (URL_ADD, self.user_logged, HTTPStatus.OK),
            (URL_LIST, self.user_logged, HTTPStatus.OK),
            (URL_SUCCESS, self.user_logged, HTTPStatus.OK),
            (URL_DETAIL, self.user_logged, HTTPStatus.NOT_FOUND),
            (URL_EDIT, self.user_logged, HTTPStatus.NOT_FOUND),
            (URL_DELETE, self.user_logged, HTTPStatus.NOT_FOUND),
            (URL_LIST, self.client, HTTPStatus.FOUND),
            (URL_ADD, self.client, HTTPStatus.FOUND),
            (URL_SUCCESS, self.client, HTTPStatus.FOUND),
            (URL_DETAIL, self.client, HTTPStatus.FOUND),
            (URL_EDIT, self.client, HTTPStatus.FOUND),
            (URL_DELETE, self.client, HTTPStatus.FOUND),
        )
        for url, client, expected_status in urls:
            with self.subTest(url=url, client=client):
                self.assertEqual(
                    client.get(url).status_code,
                    expected_status,
                )

    def test_redirects(self):
        """Проверка редиректа для неавторизованного пользователя."""
        urls = (
            (URL_LIST, REDIRECT_LIST),
            (URL_ADD, REDIRECT_ADD),
            (URL_SUCCESS, REDIRECT_SUCCESS),
            (URL_DETAIL, REDIRECT_DETAIL),
            (URL_EDIT, REDIRECT_EDIT),
            (URL_DELETE, REDIRECT_DELETE)
        )
        for url, redirect in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    redirect
                )
