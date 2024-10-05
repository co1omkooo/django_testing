from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

USER = get_user_model()
SLUG = 'note-slug'

URL_NAME = namedtuple(
    'URL_NAME',
    [
        'home',
        'add',
        'list',
        'detail',
        'edit',
        'delete',
        'success',
        'login',
        'logout',
        'signup',
    ],
)

URL = URL_NAME(
    reverse('notes:home'),
    reverse('notes:add'),
    reverse('notes:list'),
    reverse('notes:detail', args=(SLUG,)),
    reverse('notes:edit', args=(SLUG,)),
    reverse('notes:delete', args=(SLUG,)),
    reverse('notes:success'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)


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
            slug='note-slug',
            author=cls.author,
        )
