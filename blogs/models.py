from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

class Category(models.Model):
    """
    Categories for blog posts.
    """
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True, max_length=100)
    description = models.TextField(_('Description'), blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    """
    Blog post model for fitness articles.
    """
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True, max_length=200)
    content = models.TextField(_('Content'))
    excerpt = models.TextField(_('Excerpt'), blank=True, help_text=_('A short description of the blog post'))
    featured_image = models.ImageField(_('Featured Image'), upload_to='blog_images/', blank=True, null=True)
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'), related_name='blog_posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    is_published = models.BooleanField(_('Published'), default=False)
    published_at = models.DateTimeField(_('Published at'), blank=True, null=True)

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blogs:blog_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    """
    Comments on blog posts.
    """
    blog_post = models.ForeignKey(BlogPost, verbose_name=_('Blog Post'), on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField(_('Content'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    is_approved = models.BooleanField(_('Approved'), default=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog_post.title}'
