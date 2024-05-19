from django import forms
from .models import Post, Media, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class AddMediaForm(forms.ModelForm):
    file = forms.FileField(label="Файл")

    class Meta:
        model = Media
        fields = ['file',]
