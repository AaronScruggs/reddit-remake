from redditsite.models import Subreddit
from django import forms
from django.forms import Textarea


class SubredditForm(forms.ModelForm):

    class Meta:
        model = Subreddit
        fields = ("title", "description")
