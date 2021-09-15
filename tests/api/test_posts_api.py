import pytest
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Post


@pytest.mark.django_db
class TestPostsApi:
    def setup_method(self):
        self.client = APIClient()

    def test_posts_api(self):
        post = Post.objects.create(title="Test", slug="test", text="Test")
        response = self.client.get("/api/posts/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == Post.objects.count()
        assert response.data["results"][0]["title"] == post.title