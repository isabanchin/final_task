
from django.urls import path
# from content.views import *
from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<int:pk>/', views.PostView.as_view(), name='post'),
    path('post/add/', views.AddPostView.as_view(), name='add_post'),
    path('post/edit/<int:pk>/', views.EditPostView.as_view(), name='edit_post'),
    path('user/', views.UserPageView.as_view(), name='user_page'),
    path('comm/<int:pk>/', views.CommView.as_view(), name='comment'),
    path('comm/edit/<int:pk>/', views.CommView.as_view(), name='comm_edit'),
]
