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


# class AddMediaForm(forms.ModelForm):
#     class Meta:
#         model = Media
#         fields = ['file',]

#         def __init__(self, *args, **kwargs):
#             super(AddMediaForm, self).__init__(*args, **kwargs)
#             self.fields['file'].widget.attrs['multiple'] = True

# class MediaForm(forms.Form):
#     file = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={'multiple': True}))


# ----------------------------------------------------------------------
# class AddMediaInput(forms.ClearableFileInput):
#     allow_multiple_selected = True


# class AddMediaFileField(forms.FileField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault("widget", AddMediaInput())
#         super().__init__(*args, **kwargs)

#     def clean(self, data, initial=None):
#         single_file_clean = super().clean
#         if isinstance(data, (list, tuple)):
#             result = [single_file_clean(d, initial) for d in data]
#         else:
#             result = single_file_clean(data, initial)
#         return result


# class AddMediaForm(forms.Form):
#     file_field = AddMediaFileField()

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
