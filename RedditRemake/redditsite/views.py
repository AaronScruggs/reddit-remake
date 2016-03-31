from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, ListView, DetailView, CreateView
from redditsite.forms import SubredditForm, PostForm, CommentForm
from redditsite.models import Subreddit, Post, Comment
from django.core.urlresolvers import reverse, reverse_lazy


class SubredditList(ListView):
    model = Subreddit
    template_name = "redditsite/forum_list.html"
    context_object_name = "subreddits"


class SubredditDetail(DetailView):
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
        context["comments"] = self.object.comment_set.all().\
            order_by("-created_at")
        return context


class SubredditCreate(LoginRequiredMixin, CreateView):
    model = Subreddit
    form_class = SubredditForm
    success_url = reverse_lazy("list_subreddits")
    template_name = "redditsite/subreddit_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SubredditUpdate(LoginRequiredMixin, UpdateView):
    model = Subreddit
    form_class = SubredditForm
    template_name = "redditsite/subreddit_update.html"
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse("subreddit_detail", args=(self.object.id,))

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("list_subreddits")
    template_name = "redditsite/post_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "redditsite/post_update.html"
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse("post_detail", args=(self.object.id,))


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy("list_subreddits")
    template_name = "redditsite/comment_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "redditsite/comment_update.html"
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse("comment_detail", args=(self.object.id,))


class CommentDetail(DetailView):
    model = Comment
    context_object_name = "comment"
    pk_url_kwarg = "id"
