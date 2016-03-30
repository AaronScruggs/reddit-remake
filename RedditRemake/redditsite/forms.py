from redditsite.models import Subreddit, Post, Comment
from django import forms


class SubredditForm(forms.ModelForm):

    class Meta:
        model = Subreddit
        fields = ("title", "description")


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "description", "url", "subreddit")


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("comment_text", "post")
