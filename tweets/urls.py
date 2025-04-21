from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('add-restaurant/', views.add_restaurant, name='add_restaurant'),
    
    # Tweet API endpoints (keep if needed)
    path('api/tweets/', views.create_tweet, name='create_tweet'),
    path('api/tweets/<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
    path('api/tweets/<int:tweet_id>/delete/', views.delete_tweet, name='delete_tweet'),
]
