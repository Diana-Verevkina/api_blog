import pytest
from news.models import Post


class TestPostsAPI:

    @pytest.mark.django_db(transaction=True)
    def test_posts_page_not_found(self, client, post):
        response = client.get('/v1/posts/')

        assert response.status_code != 404, (
            'Страница `/v1/posts/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_list_not_auth(self, client, post):
        response = client.get('/v1/posts/')

        assert response.status_code == 200, (
            'Проверьте, что на `/v1/posts/` при запросе без токена возвращаете '
            'статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_single_not_auth(self, client, post):
        response = client.get(f'/v1/posts/{post.id}/')

        assert response.status_code == 200, (
            'Проверьте, что на `/v1/posts/{post.id}/` при запросе без токена '
            'возвращаете статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_auth(self, user_client, post):
        response = user_client.get('/v1/posts/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/v1/posts/` с токеном авторизации '
            'возвращается статус 200'
        )

        test_data = response.json()

        assert type(test_data) == list, (
            'Проверьте, что при GET запросе на `/v1/posts/` без пагинации, '
            'возвращается список'
        )

        assert len(test_data) == Post.objects.count(), (
            'Проверьте, что при GET запросе на `/v1/posts/` без пагинации '
            'возвращается весь список статей'
        )

        test_posts = test_data[0]
        assert 'id' in test_posts, (
            'Проверьте, что добавили `id` в список полей `fields` '
            'сериализатора модели Post'
        )
        assert 'header' in test_posts, (
            'Проверьте, что добавили `header` в список полей `fields` '
            'сериализатора модели Post'
        )
        assert 'text' in test_posts, (
            'Проверьте, что добавили `text` в список полей `fields` '
            'сериализатора модели Post'
        )
        assert 'pub_date' in test_posts, (
            'Проверьте, что добавили `pub_date` в список полей `fields` '
            'сериализатора модели Post'
        )
        assert 'author' in test_posts, (
            'Проверьте, что добавили `author` в список полей `fields` '
            'сериализатора модели Post'
        )
        assert 'blog' in test_posts, (
            'Проверьте, что добавили `blog` в список полей `fields` '
            'сериализатора модели Post'
        )

        assert test_posts['author'] == post.author.username, (
            'Проверьте, что `author` сериализатора модели Post возвращает '
            'имя пользователя'
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_create(self, user_client, user, another_user):
        posts_count = Post.objects.count()
        data = {}
        response = user_client.post('/v1/posts/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/v1/posts/` с неправильными '
            'данными возвращается статус 400'
        )

        data = {'header': 'test', 'text': 'test text'}
        response = user_client.post('/v1/posts/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/v1/posts/` с правильными '
            'данными возвращается статус 201'
        )
        assert (
                response.json().get('author') is not None
                and response.json().get('author') == user.username
        ), (
            'Проверьте, что при POST запросе на `/v1/posts/` автором '
            'указывается пользователь, от имени которого сделан запрос'
        )

        test_data = response.json()
        msg_error = (
            'Проверьте, что при POST запросе на `/v1/posts/` возвращается '
            'словарь с данными новой статьи'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('header') == data['header'], msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == user.username, (
            'Проверьте, что при POST запросе на `/v1/posts/` создается статья '
            'от авторизованного пользователя'
        )
        assert posts_count + 1 == Post.objects.count(), (
            'Проверьте, что при POST запросе на `/v1/posts/` создается статья'
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_get_current(self, user_client, post, user):
        response = user_client.get(f'/v1/posts/{post.id}/')

        assert response.status_code == 200, (
            'Страница `/v1/posts/{id}/` не найдена, проверьте этот адрес '
            'в *urls.py*'
        )

        test_data = response.json()
        assert test_data.get('header') == post.header, (
            'Проверьте, что при GET запросе `/v1/posts/{id}/` возвращаете '
            'данные сериализатора, не найдено или неправильное значение `header`'
        )
        assert test_data.get('text') == post.text, (
            'Проверьте, что при GET запросе `/v1/posts/{id}/` возвращаете '
            'данные сериализатора, не найдено или неправильное значение `text`'
        )
        assert test_data.get('author') == user.username, (
            'Проверьте, что при GET запросе `/v1/posts/{id}/` возвращаете '
            'данные сериализатора, не найдено или не правильное значение '
            '`author`, должно возвращать имя пользователя '
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_patch_current(self, user_client, post, another_post):
        response = user_client.patch(f'/v1/posts/{post.id}/',
                                     data={'text': 'Поменяли текст статьи'})

        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/v1/posts/{id}/` возвращаете '
            'статус 200'
        )

        test_posts = Post.objects.filter(id=post.id).first()

        assert test_posts, (
            'Проверьте, что при PATCH запросе `/v1/posts/{id}/` вы '
            'не удалили статью'
        )

        assert test_posts.text == 'Поменяли текст статьи', (
            'Проверьте, что при PATCH запросе `/v1/posts/{id}/` вы '
            'изменяете статью'
        )

        response = user_client.patch(f'/v1/posts/{another_post.id}/',
                                     data={'text': 'Поменяли текст статьи'})

        assert response.status_code == 403, (
            'Проверьте, что при PATCH запросе `/v1/posts/{id}/` для не '
            'своей статьи возвращаете статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_delete_current(self, user_client, post, another_post):
        response = user_client.delete(f'/v1/posts/{post.id}/')

        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/v1/posts/{id}/` возвращаете '
            'статус 204'
        )

        test_posts = Post.objects.filter(id=post.id).first()

        assert not test_posts, (
            'Проверьте, что при DELETE запросе `/v1/posts/{id}/` вы '
            'удалили статью'
        )

        response = user_client.delete(f'/v1/posts/{another_post.id}/')

        assert response.status_code == 403, (
            'Проверьте, что при DELETE запросе `/v1/posts/{id}/` для не своей '
            'статьи возвращаете статус 403'
        )

