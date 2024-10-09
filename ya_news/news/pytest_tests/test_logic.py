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


def test_user_can_create_comment(
        url_news_detail,
        author_client,
        author,
        news,
        redirect_detail
):
    """Авторизованный пользователь может отправить комментарий."""
    Comment.objects.all().delete()
    response = author_client.post(url_news_detail, data=form_data)
    assertRedirects(response, redirect_detail)
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
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
    admin_client,
    comment
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    response = admin_client.delete(url_comment_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author


def test_author_can_edit_comment(
    url_comment_edit,
    redirect_detail,
    comment,
    author_client
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = author_client.post(url_comment_edit, data=form_data)
    assertRedirects(response, redirect_detail)
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == form_data['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_user_cant_edit_comment_of_another_user(
    url_comment_edit,
    comment,
    admin_client
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    response = admin_client.post(url_comment_edit, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news
