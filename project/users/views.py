from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


# class LogoutUser(LogoutView):
#     def get(self, request):
#         logout(request)
#         # return redirect('home')
#         return HttpResponseRedirect(reverse('users:login'))


def logout_user(request):
    logout(request)
    # используем заданное нами в корневом и приложенческом urls.py пространство имен
    # return HttpResponseRedirect(reverse('users:login'))
    return HttpResponseRedirect(reverse('home'))
