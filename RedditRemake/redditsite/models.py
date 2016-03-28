import datetime

from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):

    user = models.OneToOneField(User, primary_key=True)

    def link_karma(self):
        """
        :return: Total link karma for user.
        """
        posts = self.user.post_set.all()
        karma = sum([post.link_karma() for post in posts])
        return karma

    def comment_karma(self):
        """
        :return: Total comment karma for user.
        """
        comments = self.user.comment_set.all()
        karma = sum([comm.total_votes() for comm in comments])
        return karma

    def average_post_upvotes(self):
        """
        :return: The average number of upvotes per post.
        """
        if not self.user.post_set.count():
            return 0

        up_count = 0
        for post in self.user.post_set.all():
            ups = post.postvote_set.filter(direction__icontains="u").count()
            up_count += ups
        return up_count / self.user.post_set.count()

    def average_post_downvotes(self):
        """
        :return: The average number of downvotes per post.
        """
        if not self.user.post_set.count():
            return 0

        down_count = 0
        for post in self.user.post_set.all():
            downs = post.postvote_set.filter(direction__icontains="d").count()
            down_count += downs
        return down_count / self.user.post_set.count()

    def average_comment_upvotes(self):
        """
        :return: The average number of upvotes per comment.
        """
        if not self.user.comment_set.count():
            return 0

        up_count = 0
        for comment in self.user.comment_set.all():
            ups = comment.commentvote_set.filter(
                direction__icontains="u").count()
            up_count += ups

        return up_count / self.user.comment_set.count()

    def average_comment_downvotes(self):
        """
        :return: The average number of downvotes per comment.
        """
        if not self.user.comment_set.count():
            return 0

        down_count = 0
        for comment in self.user.comment_set.all():
            downs = comment.commentvote_set.filter(
                direction__icontains="u").count()
            down_count += downs

        return down_count / self.user.comment_set.count()

    def total_posts(self):
        """
        :return: Total number of posts for the user.
        """
        return self.user.post_set.count()

    def total_comments(self):
        """
        :return: Total number of comments for the user.
        """
        return self.user.comment_set.count()


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
    description = models.TextField(max_length=1000,
                                   help_text="Must be over 255 characters",
                                   validators=[MinLengthValidator(256)]
                                   )

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

    def is_hot(self):
        """ True if the post has recieved 3+ comments in the past 24 hours. """
        three_hours_ago = timezone.now() - datetime.timedelta(hours=3)
        recent = self.comment_set.filter(
            created_at__gte=three_hours_ago)
        return recent.count() >= 3

    @property
    def net_votes(self):
        """ Upvotes minus downvotes. """
        downs = self.postvote_set.filter(direction__icontains="d").count()
        return self.postvote_set.count() - (downs * 2)

    def total_votes(self):
        """
        :return: Total count of all votes on this post, renamed to
         'Vote Karma' for the list display.
        """
        return self.postvote_set.count()
    total_votes.short_description = "Vote Karma"

    def link_karma(self):
        """
        If the post has a link it recieves 1 link karma for each vote.
        """
        if not self.url:
            return 0
        else:
            return self.postvote_set.count()

    def __str__(self):
        return "title: {}".format(self.title)


class Comment(models.Model):

    comment_text = models.TextField(
        max_length=1000,
        help_text="Must be over 255 characters",
        validators=[MinLengthValidator(256)])

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
        """
        :return: Total count of all votes on this comment, renamed to
         'Vote Karma' for the list display.
        """
        return self.commentvote_set.count()
    total_votes.short_description = "Vote Karma"

    def __str__(self):
        return "{}... Created on: {}".format(self.comment_text[:10],
                                             self.created_at)


class PostVote(models.Model):

    UP = "U"
    DOWN = "D"

    options = (
        (UP, "Up"),
        (DOWN, "Down")
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    direction = models.CharField(max_length=4, choices=options)

    post = models.ForeignKey(Post)

    def __str__(self):
        return "{} vote on {}".format(self.direction, self.post)


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

    def __str__(self):
        return "{} vote on {}".format(self.direction, self.comment)
