from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_categories', 'is_active', 'views', 'created_at')
    list_filter = ('is_active', 'categories', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)
    readonly_fields = ('views', 'created_at', 'updated_at')
    filter_horizontal = ('categories',)
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'content', 'image')
        }),
        ('Settings', {
            'fields': ('author', 'categories', 'is_active')
        }),
        ('Stats', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_categories(self, obj):
        return ' | '.join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'parent', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author__username', 'content', 'post__title')
    list_editable = ('is_approved',)
    readonly_fields = ('author', 'post', 'parent', 'content', 'created_at')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Approve selected comments'

    def has_add_permission(self, request):
        return False
