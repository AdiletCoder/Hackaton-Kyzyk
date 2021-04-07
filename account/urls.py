from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import *

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
