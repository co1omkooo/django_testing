"""Тест логики."""

from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

BAD_WORDS_DATA = {'text': f'Какой-то текст, {BAD_WORDS}, еще текст'}
form_data = {'text': 'Новый текст комментария'}
pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(url_news_detail, client):
    """Анонимный пользователь не может отправить комментарий."""
    client.post(url_news_detail, data=form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(url_news_detail, author_client, author, news):
    """Авторизованный пользователь может отправить комментарий."""
    expected_count = Comment.objects.count()
    response = author_client.post(url_news_detail, data=form_data)
    new_comment = Comment.objects.get()
    assertRedirects(response, f'{url_news_detail}#comments')
    assert expected_count + 1 == Comment.objects.count()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_user_cant_use_bad_words(
        url_news_detail,
        admin_client
):
    """
    Запрещенные слова.

    Если комментарий содержит запрещённые слова, он не будет опубликован,
    а форма вернёт ошибку.
    """
    assertFormError(
        admin_client.post(url_news_detail, data=BAD_WORDS_DATA),
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    url_comment_delete,
    redirect_detail,
    author_client
):
    """Авторизованный пользователь может удалять свои комментарии."""
    response = author_client.delete(url_comment_delete)
    assertRedirects(response, redirect_detail)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    url_comment_delete,
    admin_client
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    expected_count = Comment.objects.count()
    response = admin_client.delete(url_comment_delete)
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == comments_count


def test_author_can_edit_comment(
    url_comment_edit,
    redirect_detail,
    comment,
    author_client,
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = author_client.post(url_comment_edit, data=form_data)
    assertRedirects(response, redirect_detail)
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
    url_comment_edit,
    comment,
    admin_client,
    author,
    news
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    response = admin_client.post(url_comment_edit, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text
    assert comment.author == comment_from_db.author
    assert comment.news == comment_from_db.news
