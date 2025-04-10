from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_tweet, name='create_tweet'),
    path('like/<int:tweet_id>/', views.like_tweet, name='like_tweet'),
    path('delete/<int:tweet_id>/', views.delete_tweet, name='delete_tweet'),
]