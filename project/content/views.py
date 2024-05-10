from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


class PostList(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница'
    }


# LoginRequiredMixin - вход только для зарегеннных в учебных целях:
class Post(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'content/post.html'
    context_object_name = 'post'
