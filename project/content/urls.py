from django.urls import path
# from content.views import *
from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<int:pk>/', views.PostView.as_view(), name='post'),
    path('post/add/', views.AddPostView.as_view(), name='add_post'),
]
