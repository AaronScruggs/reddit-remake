from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from redditsite.forms import SubredditForm
from redditsite.models import Subreddit, Post
from django.core.urlresolvers import reverse


def list_subreddits(request):

    # link subreddit name to detail page
    subreddits = Subreddit.objects.all()
    return render(request, "redditsite/forum_list.html",
                  {"subreddits": subreddits})


def subreddit_detail(request, id):

    # Each post should link to it's detail page
    # Any post link should work as well
    subreddit = get_object_or_404(Subreddit, pk=id)
    posts = subreddit.post_set.order_by("-created_at")[:20]

    return render(request, "redditsite/forum_detail.html",
                  {"subreddit": subreddit,
                   "posts": posts})


def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    comments = post.comment_set.order_by("-created_at")

    return render(request, "redditsite/post_detail.html",
                  {"post": post,
                   "comments": comments})


class SubredditCreate(View):

    def get(self, request):
        form = SubredditForm()

        return render(request, "redditsite/subreddit_create.html", {"form": form})

    def post(self, request):
        form = SubredditForm(request.POST)

        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.user = request.user
            subreddit.save()
            return redirect(reverse("list_subreddits"))

        return render(request, "redditsite/subreddit_create.html", {"form": form})


class SubredditUpdate(View):

    def get(self, request, id):
        subreddit = get_object_or_404(Subreddit, pk=id)
        form = SubredditForm(instance=subreddit)
        return render(request, "redditsite/subreddit_update.html",
                      {"form": form, "subreddit": subreddit})

    def post(self, request, id):
        subreddit = get_object_or_404(Subreddit, pk=id)
        form = SubredditForm(data=request.POST, instance=subreddit)

        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.user = request.user
            subreddit.save()
            return redirect(reverse("list_subreddits"))
        return render(request, "redditsite/subreddit_update.html",
                      {"form": form, "subreddit": subreddit})
