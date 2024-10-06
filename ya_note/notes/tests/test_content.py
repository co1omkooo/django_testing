"""Тест контента."""

from notes.forms import NoteForm
from notes.models import Note
from notes.tests.core import (
    CoreTestCase,
    REVERSE_LIST,
    REVERSE_ADD,
    REVERSE_EDIT
)


class TestContent(CoreTestCase):
    """Тестовый класс."""

    def test_notes_list_for_different_authors(self):
        """
        Отдельная заметка.

        Отдельная заметка передаётся на страницу со списком
        заметок в списке object_list в словаре context;
        В список заметок одного пользователя не попадают
        заметки другого пользователя
        """
        response = self.author_logged.get(REVERSE_LIST)
        self.assertTrue(
            (self.note in response.context['object_list'] is True,)
        )
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_notes_list_for_different_users(self):
        """Отдельная заметка."""
        response = self.user_logged.get(REVERSE_LIST)
        self.assertTrue(
            (self.note in response.context['object_list'] is False,)
        )
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_pages_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (REVERSE_ADD, REVERSE_EDIT)
        for url in urls:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_logged.get(url).context['form'],
                    NoteForm
                )
