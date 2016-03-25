import datetime

from django.db import models
from django.core.validators import MinLengthValidator
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone


class Subreddit(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def post_count(self):
        # returns count of total posts
        return self.post_set.count()

    @property
    def today_count(self):
        # returns post count within last 24 hours
        one_day_ago = timezone.now() - datetime.timedelta(days=1)
        return self.post_set.filter(created_at__gte=one_day_ago).count()

    @property
    def daily_average(self):
        # average count of posts over the last 7 days
        one_week_ago = timezone.now() - datetime.timedelta(days=7)
        return self.post_set.filter(created_at__gte=one_week_ago).count() / 7

    def __str__(self):
        return self.title


class Post(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
        #help_text="Must be over 255 characters") #,validators=[MinLengthValidator(256)]

    url = forms.URLField(required=False) # add print
    slug = models.SlugField()  # default of 50 is fine. Required?

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    modified_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    subreddit = models.ForeignKey(Subreddit)

    @property
    def is_hot(self):
        # True if post has gotten more than 3 comments in the past 3 hours.
        three_hours_ago = timezone.now() - datetime.timedelta(hours=3)
        recent = self.comment_set.filter(created_at__gte=three_hours_ago).count()
        return recent >= 3

    def __str__(self):
        return "title: {}, created: {}".format(self.title, self.created_at)


class Comment(models.Model):

    comment_text = models.CharField(
        max_length=1000)
    #     help_text="Must be over 255 characters",
    #     validators=[MinLengthValidator(256)]
    # )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)



