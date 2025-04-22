from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, BlogPost, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'created_at')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at', 'updated_at')
    list_filter = ('is_published', 'categories', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    filter_horizontal = ('categories',)
    inlines = [CommentInline]
    actions = ['publish_posts', 'unpublish_posts']

    def publish_posts(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, _(f'{queryset.count()} posts were successfully published.'))
    publish_posts.short_description = _('Publish selected posts')

    def unpublish_posts(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, _(f'{queryset.count()} posts were successfully unpublished.'))
    unpublish_posts.short_description = _('Unpublish selected posts')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog_post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content', 'author__username', 'blog_post__title')
    date_hierarchy = 'created_at'
    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, _(f'{queryset.count()} comments were successfully approved.'))
    approve_comments.short_description = _('Approve selected comments')

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, _(f'{queryset.count()} comments were successfully disapproved.'))
    disapprove_comments.short_description = _('Disapprove selected comments')
