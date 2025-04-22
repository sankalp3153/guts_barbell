from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import BlogPost, Category, Comment

class BlogListView(ListView):
    """
    View for listing all blog posts.
    """
    model = BlogPost
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 9

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True).order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryBlogListView(ListView):
    """
    View for listing blog posts by category.
    """
    model = BlogPost
    template_name = 'blogs/category_blogs.html'
    context_object_name = 'blogs'
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return BlogPost.objects.filter(categories=self.category, is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context

class BlogDetailView(DetailView):
    """
    View for displaying a single blog post.
    """
    model = BlogPost
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True).order_by('-created_at')
        context['related_blogs'] = BlogPost.objects.filter(
            categories__in=self.object.categories.all(),
            is_published=True
        ).exclude(id=self.object.id).distinct()[:3]
        return context

@login_required
def add_comment(request, slug):
    """
    View for adding a comment to a blog post.
    """
    blog = get_object_or_404(BlogPost, slug=slug, is_published=True)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                blog_post=blog,
                author=request.user,
                content=content
            )
            messages.success(request, _('Your comment has been added successfully.'))
        else:
            messages.error(request, _('Comment cannot be empty.'))

    return redirect('blogs:blog_detail', slug=slug)
