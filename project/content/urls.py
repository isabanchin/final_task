from django.urls import path
# from content.views import *
from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<int:pk>/', views.Post.as_view(), name='post'),
]
