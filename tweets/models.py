from django.db import models
from django.utils import timezone

# Create your models here.

class Tweet(models.Model):
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='tweet_images/', null=True, blank=True)

    def __str__(self):
        return self.content