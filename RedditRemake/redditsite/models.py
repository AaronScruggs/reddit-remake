from django.db import models
from django.core.validators import MinLengthValidator
from django import forms
from django.contrib.auth.models import User


class Subreddit(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def current_count(self):
        # returns count of total posts
        pass

    def today_count(self):
        # returns posts within last 24 hours
        pass

    def daily_average(self):
        # average count of posts over the last 7 days
        pass

    def __str__(self):
        # name
        pass


class Post(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(
        max_length=1000,
        validators=[MinLengthValidator(256)]
    )
    url = forms.URLField(required=False)
    slug = models.SlugField()  # default of 50 is fine.

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    subreddit = models.ForeignKey(Subreddit)

    def is_recent(self):
        # True if created in the last 24 hours, else False
        pass

    def is_hot(self):
        # True if post has gotten more than 3 comments in the past 3 hours.
        pass


class Comment(models.Model):

    comment_text = models.CharField(
        max_length=1000,
        validators=[MinLengthValidator(256)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)


