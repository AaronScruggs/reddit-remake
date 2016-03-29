"""RedditRemake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from redditsite.views import list_subreddits, subreddit_detail, post_detail, SubredditCreate, SubredditUpdate

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^redditsite/subredditlist/$', list_subreddits, name="list_subreddits"),
    url(r'^redditsite/subredditdetail/(?P<id>\d+)/$', subreddit_detail, name="subreddit_detail"),
    url(r'^redditsite/postdetail/(?P<id>\d+)/$', post_detail, name="post_detail"),
    url(r'^redditsite/createsubreddit/$', SubredditCreate.as_view(), name="subreddit_create"),
    url(r'^redditsite/updatesubreddit/(?P<id>\d+)/$', SubredditUpdate.as_view(), name="subreddit_update"),
]
