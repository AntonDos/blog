import logging

from django.shortcuts import render

from posts.models import Post

logger = logging.getLogger(__name__)


def index_view(request):
    search = request.GET.get("search")

    posts = Post.objects.all()
    if search is not None:
        posts = posts.filter(title__icontains=search)

    return render(request, "posts/list.html", {"posts": posts})