from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, UpdateView, ListView, DetailView, CreateView
from redditsite.forms import SubredditForm, PostForm
from redditsite.models import Subreddit, Post
from django.core.urlresolvers import reverse, reverse_lazy


class SubredditList(ListView):
    model = Subreddit
    template_name = "redditsite/forum_list.html"
    context_object_name = "subreddits"


class SubredditDetail(DetailView):
    # add pagination
    model = Subreddit
    template_name = "redditsite/forum_detail.html"
    context_object_name = "subreddit"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.object.post_set.all()
        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comment_set.all().order_by("-created_at")
        return context


class SubredditCreate(LoginRequiredMixin, CreateView):
    model = Subreddit
    form_class = SubredditForm
    success_url = reverse_lazy("list_subreddits")
    template_name = "redditsite/subreddit_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SubredditUpdate(UpdateView):
    model = Subreddit
    form_class = SubredditForm
    template_name = "redditsite/subreddit_update.html"
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse("subreddit_detail", args=(self.object.id,))

###################### old post view ##############

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
