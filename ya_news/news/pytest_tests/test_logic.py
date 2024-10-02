"""Тест логики."""

from http import HTTPStatus
from random import choice

import pytest
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import COMMENT_TEXT
from pytest_django.asserts import assertFormError, assertRedirects

form_data = {'text': 'Новый текст комментария'}


def comments_before_request():
    """Количество комментариев."""
    return Comment.objects.count()


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(url_news_detail, client):
    """Анонимный пользователь не может отправить комментарий."""
    client.post(url_news_detail, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == comments_before_request()


@pytest.mark.django_db
def test_user_can_create_comment(url_news_detail, admin_client):
    """Авторизованный пользователь может отправить комментарий."""
    comments_before = comments_before_request()
    response = admin_client.post(url_news_detail, data=form_data)
    assertRedirects(response, f'{url_news_detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == comments_before + 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']


@pytest.mark.django_db
def test_user_cant_use_bad_words(url_news_detail, admin_client):
    """
    Запрещенные слова.

    Если комментарий содержит запрещённые слова, он не будет опубликован,
    а форма вернёт ошибку.
    """
    comments_before = comments_before_request()
    bad_words_data = {'text': f'Текст, {choice(BAD_WORDS)}, еще текст'}
    response = admin_client.post(url_news_detail, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == comments_before


@pytest.mark.django_db
def test_author_can_delete_comment(
    url_comment_delete,
    url_news_detail,
    author_client
):
    """Авторизованный пользователь может удалять свои комментарии."""
    comments_before = comments_before_request()
    response = author_client.delete(url_comment_delete)
    assertRedirects(response, f'{url_news_detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == comments_before - 1


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
    url_comment_delete,
    admin_client
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    comments_before = comments_before_request()
    response = admin_client.delete(url_comment_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == comments_before


@pytest.mark.django_db
def test_author_can_edit_comment(
    url_comment_edit,
    url_news_detail,
    comment,
    author_client
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = author_client.post(url_comment_edit, data=form_data)
    assertRedirects(response, f'{url_news_detail}#comments')
    comment.refresh_from_db()
    assert comment.text == 'Новый текст комментария'


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
    url_comment_edit,
    comment,
    admin_client
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    response = admin_client.post(url_comment_edit, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
