from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

USER = get_user_model()
SLUG = 'note-slug'

REVERSE_HOME = reverse('notes:home')
REVERSE_ADD = reverse('notes:add')
REVERSE_LIST = reverse('notes:list')
REVERSE_DETAIL = reverse('notes:detail', args=(SLUG,))
REVERSE_EDIT = reverse('notes:edit', args=(SLUG,))
REVERSE_DELETE = reverse('notes:delete', args=(SLUG,))
REVERSE_SUCCESS = reverse('notes:success')
REVERSE_LOGIN = reverse('users:login')
REVERSE_LOGOUT = reverse('users:logout')
REVERSE_SIGNUP = reverse('users:signup')


class CoreTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Тестовые объекты."""
        cls.author = USER.objects.create(username='Автор')
        cls.user = USER.objects.create(username='Пользователь')
        cls.author_logged = Client()
        cls.user_logged = Client()
        cls.author_logged.force_login(cls.author)
        cls.user_logged.force_login(cls.user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug=SLUG,
            author=cls.author,
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
