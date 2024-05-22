from django_filters import FilterSet
from .models import Comment

# Фильтр для страницы пользователя (по умолчанию там все его посты и все комментарии к ним)


class PostFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'post': ['exact'],
            'user': ['exact'],
            'acception': ['exact'],
            'text': ['icontent'],
        }
