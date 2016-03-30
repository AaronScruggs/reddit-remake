from redditsite.models import Subreddit, Post
from django import forms


class SubredditForm(forms.ModelForm):

    class Meta:
        model = Subreddit
        fields = ("title", "description")


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "description", "url", "subreddit")
