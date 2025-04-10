from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Tweet
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def home(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweets/home.html', {'tweets': tweets})

@csrf_exempt
def create_tweet(request):
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
            content = data.get('content')
            if content:
                tweet = Tweet.objects.create(content=content)
                return JsonResponse({'status': 'success', 'id': tweet.id})
        else:
            content = request.POST.get('content')
            image = request.FILES.get('image')
            if content:
                tweet = Tweet.objects.create(content=content, image=image if image else None)
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