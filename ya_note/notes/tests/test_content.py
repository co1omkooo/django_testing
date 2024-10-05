"""Тест контента."""

from notes.forms import NoteForm
from notes.tests.core import URL, CoreTestCase


class TestContent(CoreTestCase):
    """Тестовый класс."""

    def test_notes_list_for_different_users(self):
        """
        Отдельнгая заметка.

        Отдельная заметка передаётся на страницу со списком
        заметок в списке object_list в словаре context;
        В список заметок одного пользователя не попадают
        заметки другого пользователя
        """
        users_statuses = (
            (self.author_logged, True),
            (self.user_logged, False),
        )
        for user, status in users_statuses:
            with self.subTest(user=user):
                response = user.get(URL.list)
                self.assertTrue(
                    (self.note in response.context['object_list'] is status,
                     )
                )

    def test_pages_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (URL.add, URL.edit)
        for url in urls:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_logged.get(url).context['form'],
                    NoteForm
                )
