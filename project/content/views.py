from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Media, Comment
from .forms import AddPostForm, AddMediaForm


class PostList(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница'
    }


# LoginRequiredMixin - вход только для зарегеннных в учебных целях:
class PostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'content/post.html'
    context_object_name = 'post'


class AddPostView(CreateView):
    template_name = "content/add_post.html"
    model = Post
    form_class = AddPostForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['add_media_form'] = AddMediaForm(
                self.request.POST, self.request.FILES)
        else:
            data['add_media_form'] = AddMediaForm()
        return data

    def form_valid(self, form):
        add_media_form = AddMediaForm(self.request.POST, self.request.FILES)
        if add_media_form.is_valid():
            post = form.save(commit=False)
            post.user = self.request.user
            post.save()
            files = add_media_form.save(commit=False)
            files.post = post
            files.save()
        return super().form_valid(form)
