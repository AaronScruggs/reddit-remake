from redditsite.views import SubredditCreate, SubredditUpdate, PostCreate,\
    PostUpdate, SubredditList, SubredditDetail, PostDetail

from django.conf.urls import url

urlpatterns = [
    url(r'^subredditlist/$', SubredditList.as_view(),
        name="list_subreddits"),
    url(r'^subredditdetail/(?P<id>\d+)/$', SubredditDetail.as_view(),
        name="subreddit_detail"),
    url(r'^postdetail/(?P<id>\d+)/$', PostDetail.as_view() ,
        name="post_detail"),
    url(r'^createsubreddit/$', SubredditCreate.as_view(),
        name="subreddit_create"),
    url(r'^updatesubreddit/(?P<id>\d+)/$', SubredditUpdate.as_view(),
        name="subreddit_update"),
    url(r'^createpost/$', PostCreate.as_view(),
        name='post_create'),
    url(r'^updatepost/(?P<id>\d+)/$', PostUpdate.as_view(),
        name="post_update"),
]
