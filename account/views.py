
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User

from kyzyk import settings
from .forms import RegistrationForm
from .models import AuthToken


class RegisterView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if settings.ACTIVATE_USERS_EMAIL:
            return redirect('home')
        else:
            login(self.request, user)
            return redirect('home')


class SignInView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')


class RegisterActivateView(View):
    def get(self, request, *args, **kwargs):
        token = AuthToken.get_token(self.kwargs.get('token'))
        if token:
            if token.is_alive():
                self.activate_user(token)
            token.delete()
        return redirect('home')

    def activate_user(self, token):
        user = token.user
        user.is_active = True
        user.save()
        login(self.request, user)