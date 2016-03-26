import datetime

from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.utils import timezone


class Subreddit(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def post_count(self):
        """ Returns a count of total posts for the Subreddit. """
        return self.post_set.count()

    @property
    def today_count(self):
        """ Returns the count of posts made within the past 24 hours. """
        one_day_ago = timezone.now() - datetime.timedelta(days=1)
        return self.post_set.filter(created_at__gte=one_day_ago).count()

    @property
    def daily_average(self):
        """ The average number of post/day for the past week. """
        one_week_ago = timezone.now() - datetime.timedelta(days=7)
        return self.post_set.filter(created_at__gte=one_week_ago).count() / 7

    def __str__(self):
        return self.title


class Post(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
        #help_text="Must be over 255 characters") #,validators=[MinLengthValidator(256)]

    url = models.URLField(
                          max_length=255,
                          help_text="optional",
                          blank=True,
                          null=True
                          )

    slug = models.SlugField(
                             max_length=100,
                             blank=True,
                             null=True,
                             help_text="optional"
                            )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    modified_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    subreddit = models.ForeignKey(Subreddit)

    @property
    def is_hot(self):
        """ True if the post has recieved 3+ comments in the past 24 hours. """
        three_hours_ago = timezone.now() - datetime.timedelta(hours=3)
        recent = self.comment_set.filter(
            created_at__gte=three_hours_ago).count()
        return recent >= 3

    @property
    def net_votes(self):
        """ Upvotes minus downvotes. """
        downs = self.postvote_set.filter(direction__icontains="d").count()
        return self.postvote_set.count() - (downs * 2)


    def total_votes(self):
        return self.postvote_set.count()

    total_votes.short_description = "Vote Karma"

    def __str__(self):
        return "title: {}".format(self.title)


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

    @property
    def net_votes(self):
        """ Upvotes minus downvotes. """
        downs = self.commentvote_set.filter(direction__icontains="d").count()
        return self.commentvote_set.count() - (downs * 2)

    def total_votes(self):
        return self.commentvote_set.count()

    total_votes.short_description = "Vote Karma"


    def __str__(self):
        return "{}... Created on: {}".format(self.comment_text[:10], self.created_at)


class PostVote(models.Model):
    # created at
    # Up or down, Look up drop down option menu.
    # post vote or comment vote.
    # specific post or comment.

    UP = "U"
    DOWN = "D"

    options = (
        (UP, "Up"),
        (DOWN, "Down")
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    direction = models.CharField(max_length=4, choices=options)

    post = models.ForeignKey(Post)


class CommentVote(models.Model):

    UP = "U"
    DOWN = "D"

    options = (
        (UP, "Up"),
        (DOWN, "Down")
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    direction = models.CharField(max_length=4, choices=options)

    comment = models.ForeignKey(Comment)




