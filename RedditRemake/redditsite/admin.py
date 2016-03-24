from django.contrib import admin
from redditsite.models import Subreddit, Post, Comment

@admin.register(Subreddit)
class SubredditAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "created_at")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "url", "slug")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment_text", "created_at")




































