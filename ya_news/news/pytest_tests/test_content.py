"""Тест контента."""

import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(news_list, url_news_home, client):
    """Количество новостей на главной странице — не более 10."""
    assert (
        len(client.get(url_news_home).context['object_list'])
        == settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_news_order(url_news_home, client):
    """
    Сортировка.

    Новости отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка.
    """
    all_dates = [
        news.date for news in client.get(url_news_home).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(comments_list, url_news_detail, client, news):
    """
    Сортировка.

    Комментарии на странице отдельной новости отсортированы в хронологическом
    порядке: старые в начале списка, новые — в конце.
    """
    response = client.get(url_news_detail)
    assert 'news' in response.context
    all_comments = [comment.created for comment in news.comment_set.all()]
    assert all_comments == sorted(all_comments)


def test_anonymous_client_has_no_form(url_news_detail, client):
    """
    Форма для отправки комментария.

    Анонимному пользователю недоступна форма для отправки комментария на
    странице отдельной новости.
    """
    assert 'form' not in client.get(url_news_detail).context


def test_authorized_client_has_form(url_news_detail, author_client):
    """
    Форма для отправки комментария.

    Авторизованному пользователю доступна форма для отправки комментария на
    странице отдельной новости.
    """
    response = author_client.get(url_news_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
