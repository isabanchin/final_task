from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Media, Comment, User
from .forms import AddPostForm, FileFieldForm, AddCommentForm


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
    form = AddCommentForm()
    extra_context = {'form': form}      # передаем пустую форму в шаблон
    template_name = 'content/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(
            post=self.kwargs['pk']).values('user__username', 'text')
        context['comments'] = comments
        return context

    def post(self, request, **kwargs):
        form = AddCommentForm(request.POST)
        pk = kwargs['pk']
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post = Post.objects.get(id=pk)
            instance.save()
            return redirect('/post/' + str(pk))
        return redirect('/post/' + str(pk))
        # return redirect('post' + str(pk))


class AddPostView(LoginRequiredMixin, CreateView):
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
