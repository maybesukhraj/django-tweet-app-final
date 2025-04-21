from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(help_text="Description of the restaurant")
    address = models.CharField(max_length=200, blank=True)
    cuisine = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='restaurants/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.count() > 0:
            return sum(rating.score for rating in ratings) / ratings.count()
        return 0
    
    def review_count(self):
        return self.ratings.count()

class Rating(models.Model):
    SCORE_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    
    restaurant = models.ForeignKey(Restaurant, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=SCORE_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('restaurant', 'user')
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.score} stars"

# Keep the original Tweet model for backward compatibility
class Tweet(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='tweets/', null=True, blank=True)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:50]
