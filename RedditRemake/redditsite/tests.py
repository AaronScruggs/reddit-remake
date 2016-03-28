import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from redditsite.models import Subreddit, Post, Comment, PostVote, CommentVote


class TestSetup(TestCase):
    """
    This is a setup superclass that the test classes extend. Use this to
    create new instances of users, subreddits, posts, and comments.
    """

    # Cupcake Ipsum text to fill fields with 256 character requirements.
    cupcakes = "cupcake" * 37

    def new_user(self):
        user = User.objects.create_user(username='test',
                                        email='test@gmail.com',
                                        password='blahblah')
        return user

    def new_subreddit(self):
        subreddit = Subreddit.objects.create(title='test',
                                             description='test reddit')
        return subreddit

    def new_post(self, number, user, subreddit):
        post = Post.objects.create(title="test{}".format(number),
                                   description=self.cupcakes,
                                   user=user,
                                   subreddit=subreddit)
        return post

    def new_comment(self, number, user, post):
        comment = Comment.objects.create(user=user,
                                         post=post)
        return comment

    def new_post_vote(self, post, direction):
        return PostVote(direction=direction, post=post)

    def new_comment_vote(self, comment, direction):
        return CommentVote(comment=comment, direction=direction)


class SubredditTests(TestSetup):

    def setUp(self):
        self.user = self.new_user()
        self.subreddit = self.new_subreddit()
        self.post1 = self.new_post(1, self.user, self.subreddit)
        self.post2 = self.new_post(2, self.user, self.subreddit)

    def test_post_count(self):
        self.assertEqual(self.subreddit.post_count, 2, "Total count wrong")

    def test_today_count(self):
        old_time = timezone.now() - datetime.timedelta(days=5)
        self.post2.created_at = old_time
        self.post2.save()
        self.assertEqual(self.subreddit.today_count, 1, "Today count wrong")

    def test_daily_average(self):
        self.assertAlmostEqual(self.subreddit.daily_average,
                               2 / 7,
                               "Daily average wrong"
                               )


class PostTests(TestSetup):

    def setUp(self):
        self.user = self.new_user()
        self.subreddit = self.new_subreddit()
        self.post = self.new_post(1, self.user, self.subreddit)
        self.comment1 = self.new_comment(1, self.user, self.post)
        self.comment2 = self.new_comment(2, self.user, self.post)
        self.comment3 = self.new_comment(3, self.user, self.post)

        self.post.postvote_set.create(direction="U", post=self.post)
        self.post.postvote_set.create(direction="U", post=self.post)
        self.post.postvote_set.create(direction="D", post=self.post)

    def test_is_hot_true(self):
        self.assertTrue(self.post.is_hot(), msg="Post incorrectly not hot")

    def test_is_hot_false(self):
        old_time = timezone.now() - datetime.timedelta(days=2)
        self.comment3.created_at = old_time
        self.comment3.save()
        self.assertFalse(self.post.is_hot(), msg="Post incorrectly hot")

    def test_net_votes(self):
        self.assertEqual(self.post.net_votes, 1, msg="Vote count wrong")

    def test_total_votes(self):
        self.assertEqual(self.post.total_votes(), 3, msg="Wrong vote total")


class CommentTests(TestSetup):

    def setUp(self):
        self.user = self.new_user()
        self.subreddit = self.new_subreddit()
        self.post = self.new_post(1, self.user, self.subreddit)
        self.comment = self.new_comment(1, self.user, self.post)

        self.comment.commentvote_set.create(direction="U",
                                            comment=self.comment)
        self.comment.commentvote_set.create(direction="D",
                                            comment=self.comment)
        self.comment.commentvote_set.create(direction="D",
                                            comment=self.comment)

    def test_net_votes(self):
        self.assertEqual(self.comment.net_votes, -1, msg="Wrong net votes")

    def test_total_votes(self):
        self.assertEqual(self.comment.total_votes(), 3, msg="Wrong vote total")
