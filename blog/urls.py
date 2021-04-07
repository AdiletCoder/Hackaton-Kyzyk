from django.urls import path

from blog.views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('<str:slug>/', PostListView.as_view(), name='list'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='detail'),
    path('post/<str:slug>/add_comment/',  ReviewPostCreateView.as_view(), name='add_comment'),
    path('post/<str:slug>/list_comments/', ReviewIndexPage.as_view(), name='list_comments'),
    path('post/create', PostCreateView.as_view(), name='create-post'),
    path('post/update/<str:slug>/', PostUpdateView.as_view(), name='update-post'),
    path('post/delete/<str:slug>/', PostDeleteView.as_view(), name='delete-post'),
    path('search', SearchListView.as_view(), name='search'),
    path('like/<str:slug>', LikeView, name='like_post'),
]