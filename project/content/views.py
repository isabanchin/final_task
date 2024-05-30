# from pathlib import Path
# from typing import Any
# from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Media, Comment
from .forms import AddPostForm, FileFieldForm, AddCommentForm, AcceptCommentForm
from .filters import CommentFilter
from itertools import chain
from django.core.mail import EmailMultiAlternatives


class PostList(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = 'posts'
    # paginate_by = 6
    extra_context = {
        'title': 'Главная страница'
    }


# LoginRequiredMixin - вход только для зарегеннных в учебных целях:
class PostView(LoginRequiredMixin, DetailView):
    model = Post
    comm_form = AddCommentForm()                                #
    # передаем пустую форму в шаблон
    extra_context = {'comm_form': comm_form}
    template_name = 'content/post.html'
    context_object_name = 'post'

# Добавляем в контекст утвержденные комментарии поста, для автора поста все комментарии, для автора комментария все собственные комменты:
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        comments = list(chain(Comment.objects.filter(
            post=pk, acception=True).values('user__username', 'text', 'acception'), Comment.objects.filter(
            post=pk, user=self.request.user, acception=False).values('user__username', 'text', 'acception')))  # (сцепляем два запроса в которых обращаемся к связанной модели User)
        context['comments'] = comments
        # добавляем в контекст ранее загруженные картинки:
        context['image_objects'] = Media.objects.filter(
            post=pk, file_type='img')
        # добавляем в контекст ранее загруженные файлы:
        context['file_objects'] = Media.objects.filter(
            post=pk, file_type='file')
        context['video_objects'] = Media.objects.filter(
            post=pk, file_type='video')
        context['add_media_form'] = FileFieldForm()
        return context

# сохраняем комментарий и возвращаемся на страницу поста
    def post(self, request, **kwargs):
        pk = kwargs['pk']
        if request.POST.get('post_edit'):
            return redirect('edit_post', pk)
        if request.POST.get('text'):
            form = AddCommentForm(request.POST)
            if form.is_valid():                                             #
                instance = form.save(commit=False)
                instance.user = request.user
                instance.post = Post.objects.get(id=pk)
                # если автор комментария и поста совпадает, то комментарий утверждается:
                if instance.user == Post.objects.get(id=pk).user:
                    instance.acception = True
                instance.save()    # сохраняем новый комментарий в БД
                if instance.user != Post.objects.get(id=pk).user:
                    # comment = Comment.objects.filter(id=pk)
                    # формируем данные для уведомления и отправляем email:
                    html_content = render_to_string('content/email_new_comment.html', {
                        'comment': instance,
                        'post_url': f'http://127.0.0.1:8000/{instance.post.get_absolute_url()}',
                    })  # формируем строку html-шаблона письма
                    msg = EmailMultiAlternatives(
                        subject=f'Новый комментарий к Вашему посту "{instance.post}"',
                        body=f'К Вашему посту "{instance.post}" добавлен новый комментарий автора {instance.user}: "{instance.text}"',
                        from_email='sabanchini@yandex.ru',
                        to=[instance.post.user.email]
                    )
                    msg.attach_alternative(
                        html_content, "text/html")  # добавляем html
                    msg.send()  # отсылаем
        return redirect('/post/' + str(pk))


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
            extension = f.name.split('.')[-1]
            if extension in ['jpg', 'jpeg', 'bmp', 'png', 'gif']:
                Media.objects.create(file=f, post=post_form, file_type='img')
            else:
                Media.objects.create(file=f, post=post_form, file_type='file')
        return super().form_valid(form)


class UserPageView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = "content/user_page.html"
    context_object_name = 'comments'
    ordering = ['-time']
    extra_context = {
        'title': 'Ваша страница'
    }

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст
        context['filter'] = CommentFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class CommView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'content/comment.html'
    context_object_name = 'comment'
    extra_context = {'del_confirmation': ""}

    def post(self, request, **kwargs):
        pk = kwargs['pk']
        self.extra_context['del_confirmation'] = ""
# обработка формы "acception"
        if self.request.POST.get('acception'):
            if self.request.POST.get('acception') == 'accept':
                instance = Comment.objects.filter(
                    id=pk).update(acception=False)
                comment = Comment.objects.get(id=pk)
                print('comment.post.get_absolute_url() =',
                      comment.post.get_absolute_url())
                # формируем данные для уведомления и отправляем email:
                html_content = render_to_string('content/email_comment_acception.html', {
                    'comment': comment,
                    'post_url': f'http://127.0.0.1:8000/{comment.post.get_absolute_url()}',
                })  # формируем строку html-шаблона письма
                msg = EmailMultiAlternatives(
                    subject=f'Ваш комментарий к посту "{comment.post}" принят',
                    body=f'Ваш комментарий к посту "{comment.post}" принят автором и доступен для просмотра другими пользователями: "{comment.text}"',
                    from_email='sabanchini@yandex.ru',
                    to=[comment.user.email]
                )
                msg.attach_alternative(
                    html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем
                return redirect('comment', pk)
            # фиксируем "удалить"
            elif self.request.POST.get('acception') == 'delete':
                # заменить на (redirect to 'com_dell'):
                self.extra_context['del_confirmation'] = "request"
                return redirect('comment', pk)
        # обработка формы "confirm" для удаления
        if self.request.POST.get('confirm'):
            # при подтверждении удаляем
            if self.request.POST.get('confirm') == 'delete_confirmed':
                Comment.objects.filter(id=pk).delete()
                return redirect('user_page')
            # при отмене - назад
            elif self.request.POST.get('confirm') == 'delete_cancel':
                return redirect('comment', pk)
# обработка кнопки "edit"
        if self.request.POST.get('edit'):
            self.extra_context['edit'] = "yes"
            return redirect('comment', pk)
# сохранение новой редакции комментария
        if self.request.POST.get('comm_edit'):
            instance = Comment.objects.filter(id=pk).update(
                text=self.request.POST.get('comm_edit'))
            self.extra_context['edit'] = "no"
            return redirect('comment', pk)


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'content/add_post.html'
    fields = ['category', 'title', 'text']

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        data = super().get_context_data(**kwargs)
        # добавляем в контекст ранее загруженные картинки:
        data['image_objects'] = Media.objects.filter(
            post=pk, file_type='img')
        # добавляем в контекст ранее загруженные файлы:
        data['file_objects'] = Media.objects.filter(
            post=pk, file_type='file')
        data['video_objects'] = Media.objects.filter(
            post=pk, file_type='video')
        data['add_media_form'] = FileFieldForm()
        return data

    def post(self, request, pk):
        # обрабатываем запрос только для юзера равного автору:
        if self.request.user == Post.objects.get(id=pk).user:
            # удаление файлов:
            if self.request.POST.get('del_file'):
                instance = Media.objects.get(
                    file=self.request.POST.get('del_file'))
                instance.delete()
            else:
                post_form = self.request.POST
                p = Post.objects.get(id=pk)
                p.category = post_form['category']
                p.title = post_form['title']
                p.text = post_form['text']
                p.user = self.request.user
                post = p.save()
                # сохраняем файлы:
                files = request.FILES.getlist('file_field')
                for f in files:
                    extension = f.name.split('.')[-1]
                    if extension in ['jpg', 'jpeg', 'bmp', 'png', 'gif']:
                        f_type = 'img'
                    elif extension in ['mp4', 'mov']:
                        f_type = 'video'
                    else:
                        f_type = 'file'
                    Media.objects.create(
                        post=p, file=f, file_type=f_type)
        else:
            return redirect('home')
        return redirect('edit_post', pk)

    # def form_valid(self, form):
    #     cd = form.cleaned_data
    #     print('cd = ', cd)
    #     pk = self.kwargs['pk']
    #     # сохраняем форму только для юзера равного автору:
    #     if self.request.user == Post.objects.get(id=pk).user:
    #         # сохраняем форму поста
    #         print('self.request.POST = ', dir(self.request.POST))
    #         post_form = form.save(commit=False)
    #         post_form.user = self.request.user
    #         post_form.save()
    #         # сохраняем файлы
    #         files = self.request.FILES.getlist('file_field')
    #         for f in files:
    #             extension = f.name.split('.')[-1]
    #             if extension in ['jpg', 'jpeg', 'bmp', 'png', 'gif']:
    #                 Media.objects.create(
    #                     file=f, post=post_form, file_type='img')
    #             else:
    #                 Media.objects.create(
    #                     file=f, post=post_form, file_type='file')
    #         # удаление файлов не срабатывает так как ничто не инициирует валидацию:
    #         if self.request.POST.get('del_file'):
    #             print('файлы к удалению', self.request.POST.get('del_file'))
    #             print('условие уделения файлов')
    #             instance = Media.objects.get(
    #                 file=self.request.POST.get('del_file'))
    #             instance.delete()
    #             print('post-запрос')
    #             return redirect('edit_post', pk)
    #         return super().form_valid(form)
    #     else:
    #         return redirect('home')

    # def get_success_url(self):
    #     # pk = self.kwargs['pk']
    #     # print('get_success_url')
    #     return reverse('edit_post', kwargs={'pk': self.kwargs['pk']})
    #     # return redirect('edit_post', pk)
