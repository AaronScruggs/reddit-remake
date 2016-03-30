from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from redditsite.forms import SubredditForm, PostForm
from redditsite.models import Subreddit, Post
from django.core.urlresolvers import reverse


class SubredditList(View):

    def get(self, request):
        """
        :return: A clickable list of all subreddits.
        """
        subreddits = Subreddit.objects.all()

        return render(request, "redditsite/forum_list.html",
                      {"subreddits": subreddits})


class SubredditDetail(View):

    def get(self, request, id):
        """
        :return: Information on a specific subreddit page.
        """
        subreddit = get_object_or_404(Subreddit, pk=id)
        posts = subreddit.post_set.order_by("-created_at")[:20]

        return render(request, "redditsite/forum_detail.html",
                      {"subreddit": subreddit,
                       "posts": posts})


class PostDetail(View):

    def get(self, request, id):
        """
        :return: Information on a specific post page.
        """
        post = get_object_or_404(Post, pk=id)
        comments = post.comment_set.order_by("-created_at")

        return render(request, "redditsite/post_detail.html",
                      {"post": post,
                       "comments": comments})


class SubredditCreate(View):
    """
    This is a class view for creating a new subreddit.
    """

    def get(self, request):
        form = SubredditForm()

        return render(request, "redditsite/subreddit_create.html",
                      {"form": form})

    def post(self, request):
        form = SubredditForm(request.POST)

        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.user = request.user
            subreddit.save()
            return redirect(reverse("list_subreddits"))

        return render(request, "redditsite/subreddit_create.html",
                      {"form": form})


class SubredditUpdate(View):
    """
    Use for updating an existing subreddit.
    """

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


class PostCreate(View):
    def get(self, request):
        form = PostForm()

        return render(request, "redditsite/post_create.html",
                      {"form": form})

    def post(self, request):
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse("list_subreddits"))

        return render(request, "redditsite/post_create.html",
                      {"form": form})


class PostUpdate(View):
    def get(self, request, id):
        post = get_object_or_404(Post, pk=id)
        form = PostForm(instance=post)
        return render(request, "redditsite/post_update.html",
                      {"form": form, "post": post})

    def post(self, request, id):
        post = get_object_or_404(Post, pk=id)
        form = PostForm(data=request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse("list_subreddits"))
        return render(request, "redditsite/post_update.html",
                      {"form": form, "post": post})
