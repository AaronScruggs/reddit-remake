from django.shortcuts import render, get_object_or_404
from redditsite.models import Subreddit, Post


def list_subreddits(request):

    # link subreddit name to detail page
    subreddits = Subreddit.objects.all()
    return render(request, "redditsite/forum_list.html", {"subreddits": subreddits})


def subreddit_detail(request, id):

    # Each post should link to it's detail page
    # Any post link should work as well
    subreddit = get_object_or_404(Subreddit, pk=id)
    posts = subreddit.post_set.order_by("-created_at")

    return render(request, "redditsite/forum_detail.html",
                  {"subreddit": subreddit,
                   "posts": posts})



def post_detail(request, id):

    # is recent
    # is hot
    # list the comments
    post = get_object_or_404(Post, pk=id)

    return render(request, "redditsite/post_detail.html", {"post": post})











