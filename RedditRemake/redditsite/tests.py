import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from redditsite.models import Subreddit, Post, Comment


class SubredditTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='test',
                                             email='test@gmail.com',
                                             password='blahblah')

        self.subreddit = Subreddit.objects.create(title='test',
                                                  description='test reddit')
        self.post1 = Post.objects.create(title='test1',
                                         description='test post1',
                                         user=self.user,
                                         subreddit=self.subreddit
                                         )
        self.post2 = Post.objects.create(title="test2",
                                         description="test post2",
                                         user=self.user,
                                         subreddit=self.subreddit
                                         )

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


class PostTests(TestCase):

    def setUp(self):
        pass

    def test_is_hot(self):
        pass

    def test_net_votes(self):
        pass

    def test_total_votes(self):
        pass



class CommentTests(TestCase):

    def setUp(self):
        pass

    def test_net_votes(self):
        pass

    def test_total_votes(self):
        pass



























