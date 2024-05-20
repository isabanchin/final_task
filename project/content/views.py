from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Media, Comment
from .forms import AddPostForm, FileFieldForm


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
    model = Post
    form_class = AddPostForm
    template_name = 'content/add_post.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['add_media_form'] = FileFieldForm(
                self.request.POST, self.request.FILES)
        else:
            data['add_media_form'] = FileFieldForm()
        return data

    def form_valid(self, form):
        post_form = form.save(commit=False)
        post_form.user = self.request.user
        post_form.save()
        files = self.request.FILES.getlist('file_field')
        for f in files:
            Media.objects.create(file=f, post=post_form)
        return super().form_valid(form)
