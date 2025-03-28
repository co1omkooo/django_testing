"""Тест логики."""

from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.core import (
    CoreTestCase,
    URL_ADD,
    URL_SUCCESS,
    URL_EDIT,
    URL_DELETE,
    REDIRECT_ADD
)


class TestCommentCreation(CoreTestCase):
    """Тестовый класс."""

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        Note.objects.all().delete()
        self.assertRedirects(
            self.author_logged.post(
                URL_ADD,
                data=self.form_data
            ),
            URL_SUCCESS
        )
        self.assertEqual(1, Note.objects.count())
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        note_before = Note.objects.all()
        response = self.client.post(URL_ADD, data=self.form_data)
        self.assertRedirects(response, REDIRECT_ADD)
        note_after = Note.objects.all()
        self.assertEqual(set(note_before), set(note_after))

    def test_not_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        note_before = Note.objects.all()
        self.form_data['slug'] = self.note.slug
        response = self.author_logged.post(
            URL_ADD,
            data=self.form_data
        )
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        note_after = Note.objects.all()
        self.assertEqual(set(note_before), set(note_after))

    def test_empty_slug(self):
        """
        Формирование slug.

        Если при создании заметки не заполнен slug, то он формируется
        автоматически, с помощью функции pytils.translit.slugify.
        """
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_logged.post(
            URL_ADD,
            data=self.form_data
        )
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(1, Note.objects.count())
        new_note = Note.objects.get()
        self.assertEqual(new_note.slug, slugify(self.form_data['title']))
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        """Пользователь может редактировать свои заметки."""
        response = self.author_logged.post(
            URL_EDIT,
            data=self.form_data
        )
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get(id=self.note.id)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        """Пользователь не может редактировать чужие заметки."""
        response = self.user_logged.post(
            URL_EDIT,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        """Пользователь может удалять свои заметки."""
        note_old = Note.objects.count()
        response = self.author_logged.post(URL_DELETE)
        self.assertRedirects(response, URL_SUCCESS)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
        self.assertEqual(Note.objects.count(), note_old - 1)

    def test_other_user_cant_delete_note(self):
        """Пользователь не может удалять чужие заметки."""
        response = self.user_logged.post(URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)
