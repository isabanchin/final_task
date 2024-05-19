from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from .forms import LoginUserForm, RegisterUserForm


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


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


# def register(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})
