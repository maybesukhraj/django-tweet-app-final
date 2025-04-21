from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

# Import models from models.py, not define them here
from .models import Tweet, Restaurant, Rating
from .forms import RestaurantForm, RatingForm

def home(request):
    """
    Home view that displays restaurants with search functionality
    """
    query = request.GET.get('q')
    if query:
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) |
            Q(content__icontains=query) |
            Q(cuisine__icontains=query) |
            Q(address__icontains=query)
        )
    else:
        restaurants = Restaurant.objects.all().order_by('-created_at')
    
    return render(request, 'tweets/home.html', {
        'restaurants': restaurants,
        'query': query
    })

def restaurant_detail(request, pk):
    """
    View for restaurant details and adding reviews
    """
    restaurant = get_object_or_404(Restaurant, pk=pk)
    rating_form = RatingForm()
    user_rating = None
    
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(restaurant=restaurant, user=request.user).first()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if user_rating:
            # Update existing rating
            rating_form = RatingForm(request.POST, instance=user_rating)
        else:
            # Create new rating
            rating_form = RatingForm(request.POST)
        
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.restaurant = restaurant
            rating.user = request.user
            rating.save()
            return redirect('restaurant_detail', pk=pk)
    
    # If user has already rated, show their rating in the form
    if user_rating and request.method == 'GET':
        rating_form = RatingForm(instance=user_rating)
    
    return render(request, 'tweets/restaurant_detail.html', {
        'restaurant': restaurant,
        'rating_form': rating_form,
        'reviews': restaurant.ratings.order_by('-created_at'),
        'user_rating': user_rating
    })

@login_required
def add_restaurant(request):
    """
    View for adding a new restaurant
    """
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save()
            return redirect('restaurant_detail', pk=restaurant.pk)
    else:
        form = RestaurantForm()
    
    return render(request, 'tweets/add_restaurant.html', {'form': form})

def search(request):
    """
    Search view - redirects to home with query parameter
    """
    query = request.GET.get('q', '')
    return redirect(f'/?q={query}')

# Original tweet functionality (keep if needed)
@csrf_exempt
def create_tweet(request):
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
            content = data.get('content')
        else:
            content = request.POST.get('content')
            image = request.FILES.get('image')
            
        if content:
            tweet = Tweet.objects.create(
                content=content,
                image=image if 'image' in locals() else None
            )
            return JsonResponse({'status': 'success', 'id': tweet.id})
    return JsonResponse({'status': 'error'})

@csrf_exempt
def like_tweet(request, tweet_id):
    if request.method == 'POST':
        try:
            tweet = Tweet.objects.get(id=tweet_id)
            tweet.likes += 1
            tweet.save()
            return JsonResponse({'status': 'success', 'likes': tweet.likes})
        except Tweet.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

@csrf_exempt
def delete_tweet(request, tweet_id):
    if request.method == 'POST':
        try:
            tweet = get_object_or_404(Tweet, id=tweet_id)
            tweet.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
