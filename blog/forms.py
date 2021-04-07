from django import forms
from .models import Post, ReviewPost
from django.contrib.auth.models import User


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'slug', 'body', 'image', 'tags',)

        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'slug': forms.SlugField(attrs={'class': 'form-control'}),
        #     'body': forms.Textarea(attrs={'class': 'form-control'}),
        #     'image': forms.ImageField(attrs={'class': 'form-control'}),
        #     'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        # }


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewPost
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


