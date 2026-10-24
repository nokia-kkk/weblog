from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import re


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=300, verbose_name='Title')
    content = RichTextField(verbose_name='Content')
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='Cover Image')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    categories = models.ManyToManyField(Category, blank=True, verbose_name='Categories')
    is_active = models.BooleanField(default=True, verbose_name='Published')
    views = models.PositiveIntegerField(default=0, verbose_name='Views')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Published Date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_excerpt(self, word_count=30):
        plain = re.sub(r'<[^>]+>', '', self.content)
        words = plain.split()
        if len(words) <= word_count:
            return plain
        return ' '.join(words[:word_count]) + '...'

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_approved_comments(self):
        return self.comments.filter(is_approved=True, parent=None)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Post')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='Reply To')
    content = models.TextField(verbose_name='Comment')
    is_approved = models.BooleanField(default=False, verbose_name='Approved')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_replies(self):
        return self.replies.filter(is_approved=True)
