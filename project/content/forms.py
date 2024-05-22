from django import forms
from django.forms import ModelForm
from .models import Post, Media, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

# Добавление поста:


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class FileFieldForm(forms.Form):
    file_field = MultipleFileField(required=False)

# Добавление комментария:


class AddCommentForm(ModelForm):
    text = forms.CharField(label='Оставить комментарий', widget=forms.Textarea(
        attrs={'cols': 70, 'rows': 4}), required=True)

    class Meta:
        model = Comment
        fields = ['text',]
