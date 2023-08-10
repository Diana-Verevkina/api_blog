import pytest
from ...news.models import Post, Follow


@pytest.fixture
def post(user):
    return Post.objects.create(text='Тестовый пост 1', author=user,)


@pytest.fixture
def post_2(user):
    return Post.objects.create(text='Тестовый пост 2', author=user,)


@pytest.fixture
def another_post(another_user):
    return Post.objects.create(text='Тестовый пост 3', author=another_user,)


@pytest.fixture
def follow_1(user, another_user):
    return Follow.objects.create(user=user, author=another_user)


@pytest.fixture
def follow_2(user_2, user):
    return Follow.objects.create(user=user_2, author=user)


@pytest.fixture
def follow_3(user_2, another_user):
    return Follow.objects.create(user=user_2, author=another_user)


@pytest.fixture
def follow_4(another_user, user):
    return Follow.objects.create(user=another_user, author=user)


@pytest.fixture
def follow_5(user_2, user):
    return Follow.objects.create(user=user, author=user_2)
