"""Тест контента."""

from notes.forms import NoteForm
from notes.tests.core import (
    CoreTestCase,
    URL_LIST,
    URL_ADD,
    URL_EDIT
)


class TestContent(CoreTestCase):
    """Тестовый класс."""

    def test_notes_list_for_different_authors(self):
        """
        Отдельная заметка.

        Отдельная заметка передаётся на страницу со списком
        заметок в списке object_list в словаре context.
        """
        response = self.author_logged.get(URL_LIST)
        self.assertIn(self.note, response.context['object_list'])
        object_list = response.context['object_list'].get(id=self.note.id)
        self.assertEqual(self.note.title, object_list.title)
        self.assertEqual(self.note.text, object_list.text)
        self.assertEqual(self.note.slug, object_list.slug)
        self.assertEqual(self.note.author, object_list.author)

    def test_notes_do_not_get_to_another_user(self):
        """
        Отдельная заметка.

        В список заметок одного пользователя не попадают
        заметки другого пользователя.
        """
        response = self.user_logged.get(URL_LIST)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_pages_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (URL_ADD, URL_EDIT)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_logged.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
