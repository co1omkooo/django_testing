"""Тесты маршрутов."""

from http import HTTPStatus

from notes.tests.core import URL, CoreTestCase


class TestRoutes(CoreTestCase):
    """Тестовый класс."""

    def test_pages_availability_for_anonymous_user(self):
        """Проверка доступа к страницам."""
        urls = (
            (URL.home, self.client, HTTPStatus.OK, 'anonim'),
            (URL.login, self.client, HTTPStatus.OK, 'anonim'),
            (URL.logout, self.client, HTTPStatus.OK, 'anonim'),
            (URL.signup, self.client, HTTPStatus.OK, 'anonim'),
            (URL.detail, self.author_logged, HTTPStatus.OK, 'Автор'),
            (URL.edit, self.author_logged, HTTPStatus.OK, 'Автор'),
            (URL.delete, self.author_logged, HTTPStatus.OK, 'Автор'),
            (URL.add, self.user_logged, HTTPStatus.OK, 'Пользователь'),
            (URL.list, self.user_logged, HTTPStatus.OK, 'Пользователь'),
            (URL.success, self.user_logged, HTTPStatus.OK, 'Пользователь'),
            (
                URL.detail,
                self.user_logged,
                HTTPStatus.NOT_FOUND,
                'Пользователь'
            ),
            (
                URL.edit,
                self.user_logged,
                HTTPStatus.NOT_FOUND,
                'Пользователь'
            ),
            (
                URL.delete,
                self.user_logged,
                HTTPStatus.NOT_FOUND,
                'Пользователь'
            ),
        )
        for url, client, expected_status, user in urls:
            with self.subTest(url=url):
                self.assertEqual(
                    client.get(url).status_code,
                    expected_status,
                    msg=(
                        f'Код ответа страницы {url} для {user} не '
                        f'соответствует ожидаемому.'
                    ),
                )

    def test_redirects(self):
        """Проверка редиректа для неавторизованного пользователя."""
        urls = (
            URL.list,
            URL.add,
            URL.success,
            URL.detail,
            URL.edit,
            URL.delete,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{URL.login}?next={url}'
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url,
                    msg_prefix=(
                        f'Убедитесь, что у неавторизованного '
                        f'пользователя нет доступа к странице {url}.'
                    ),
                )
