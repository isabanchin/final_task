from django.urls import path
from content.views import *
# from .content import views


urlpatterns = [
    path('', PostList.as_view(), name='home')
]