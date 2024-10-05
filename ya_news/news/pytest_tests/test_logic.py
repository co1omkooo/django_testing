"""Тест логики."""

from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING
from news.models import Comment


form_data = {'text': 'Новый текст комментария'}
pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(url_news_detail, client):
    """Анонимный пользователь не может отправить комментарий."""
    client.post(url_news_detail, data=form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(url_news_detail, author_client, author, news):
    """Авторизованный пользователь может отправить комментарий."""
    expected_count = Comment.objects.count() + 1
    response = author_client.post(url_news_detail, data=form_data)
    new_comment = Comment.objects.get()
    assertRedirects(response, f'{url_news_detail}#comments')
    assert expected_count == Comment.objects.count()
    assert all(
        (
            new_comment.text == form_data['text'],
            new_comment.author == author,
            new_comment.news == news,
        )
    )


def test_user_cant_use_bad_words(
        url_news_detail,
        admin_client,
        bad_words_data
):
    """
    Запрещенные слова.

    Если комментарий содержит запрещённые слова, он не будет опубликован,
    а форма вернёт ошибку.
    """
    response = admin_client.post(url_news_detail, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    url_comment_delete,
    url_news_detail,
    author_client
):
    """Авторизованный пользователь может удалять свои комментарии."""
    response = author_client.delete(url_comment_delete)
    assertRedirects(response, f'{url_news_detail}#comments')
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    url_comment_delete,
    admin_client
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    response = admin_client.delete(url_comment_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
    url_comment_edit,
    url_news_detail,
    comment,
    author_client,
    news,
    author
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = author_client.post(url_comment_edit, data=form_data)
    assertRedirects(response, f'{url_news_detail}#comments')
    comment.refresh_from_db()
    assert all(
        (
            comment.text == form_data['text'],
            comment.news == news,
            comment.author == author,
        )
    )


def test_user_cant_edit_comment_of_another_user(
    url_comment_edit,
    comment,
    admin_client
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    response = admin_client.post(url_comment_edit, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'
