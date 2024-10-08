from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

USER = get_user_model()
SLUG = 'note-slug'

URL_HOME = reverse('notes:home')
URL_ADD = reverse('notes:add')
URL_LIST = reverse('notes:list')
URL_DETAIL = reverse('notes:detail', args=(SLUG,))
URL_EDIT = reverse('notes:edit', args=(SLUG,))
URL_DELETE = reverse('notes:delete', args=(SLUG,))
URL_SUCCESS = reverse('notes:success')
URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')
REDIRECT_ADD = f'{URL_LOGIN}?next={URL_ADD}'
REDIRECT_LIST = f'{URL_LOGIN}?next={URL_LIST}'
REDIRECT_SUCCESS = f'{URL_LOGIN}?next={URL_SUCCESS}'
REDIRECT_DETAIL = f'{URL_LOGIN}?next={URL_DETAIL}'
REDIRECT_EDIT = f'{URL_LOGIN}?next={URL_EDIT}'
REDIRECT_DELETE = f'{URL_LOGIN}?next={URL_DELETE}'


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
