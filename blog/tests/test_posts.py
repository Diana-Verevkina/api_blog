import pytest
from


class TestPostsAPI:

    @pytest.mark.django_db(transaction=True)
    def test_posts_page_not_found(self, client, post):
        response = client.get('/v1/posts/')

        assert response.status_code != 404, (
            'Страница `/v1/news/` не найдена, проверьте этот адрес в *urls.py*'
        )

