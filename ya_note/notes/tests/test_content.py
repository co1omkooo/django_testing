"""Тест контента."""

from notes.forms import NoteForm
from notes.models import Note
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
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_notes_do_not_get_to_another_user(self):
        """
        Отдельная заметка.

        В список заметок одного пользователя не попадают
        заметки другого пользователя.
        """
        response = self.user_logged.get(URL_LIST)
        self.assertNotIn(self.note, response.context['object_list'])
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_pages_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (URL_ADD, URL_EDIT)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_logged.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
