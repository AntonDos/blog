from django.http import HttpResponse
from django.shortcuts import render

from posts.forms import RegistrationForm
from posts.models import Post


def index(request):
    title = request.GET.get("title")

    if request.user.is_authenticated:
        post_list = Post.objects.filter(author=request.user)
    else:
        post_list = Post.objects.all()

    if title is not None:
        post_list = post_list.filter(title__contains=title)

    post_titles = [post.title for post in post_list]
    return HttpResponse(", ".join(post_titles))


def register(request):
    form = RegistrationForm()
    return render(request, "base.html", {"form": form})