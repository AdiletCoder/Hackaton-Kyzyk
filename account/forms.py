from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse

from account.models import AuthToken
from kyzyk import settings


# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(min_length=6, required=True, widget=forms.PasswordInput)
#     password_confirmation = forms.CharField(min_length=6, required=True, widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password_confirmation', 'email', 'first_name', 'last_name')
#
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError('User with this username already exists')
#         return username
#
#     def clean(self):
#         data = self.cleaned_data
#         password = data.get('password')
#         password_confirm = data.pop('password_confirmation')
#         if password != password_confirm:
#             raise forms.ValidationError('Passwords did not match')
#         else:
#             return data
#
#     def save(self, commit=True):
#         user = User.objects.create_user(**self.cleaned_data)
#         return user
#

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']

    def save(self, commit=True):
        if settings.ACTIVATE_USERS_EMAIL:
            user: AbstractUser = super().save(commit=False)
            user.is_active = False
            if commit:
                user.save()
                token = self.create_token(user)
                self.send_email(user, token)
        else:
            user = super().save(commit=commit)
        return user

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('User with this username already exists')
        return username

    def clean(self):
        data = self.cleaned_data
        password = data.get('password1')
        password_confirm = data.pop('password2')
        if password != password_confirm:
            raise forms.ValidationError('Passwords did not match')
        else:
            return data

    def create_token(self, user):
        return AuthToken.objects.create(user=user)

    def send_email(self, user, token):
        if user.email:
            subject = 'Вы создали учётную запись на сайте "Kyzyk-Life"'
            link = settings.BASE_HOST + reverse('activate', kwargs={'token': token.token})
            message = f'''Здравствуйте, {user.username}!
Вы создали учётную запись на сайте "Kyzyk-Life"
Активируйте её, перейдя по ссылке {link}.
Если вы считаете, что это ошибка, просто игнорируйте это письмо.'''
            html_message = f'''Здравствуйте, {user.username}!
Вы создали учётную запись на сайте "Kyzyk-Life"
Активируйте её, перейдя по ссылке <a href="{link}">{link}</a>.
Если вы считаете, что это ошибка, просто игнорируйте это письмо.'''
            try:
                user.email_user(subject, message, html_message=html_message)
            except Exception as e:
                print(e)