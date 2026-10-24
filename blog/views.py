from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def rooms(request):
    return render(request, 'rooms.html')


def elements(request):
    return render(request, 'elements.html')


def contact(request):
    return render(request, 'contact.html')


def blog(request):
    posts = Post.objects.filter(is_active=True)
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()

    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(categories__id=category_id)

    author_id = request.GET.get('author')
    if author_id:
        posts = posts.filter(author_id=author_id)

    date_filter = request.GET.get('date')
    if date_filter:
        try:
            year, month = date_filter.split('-')
            posts = posts.filter(created_at__year=year, created_at__month=month)
        except (ValueError, AttributeError):
            pass

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recent_posts = Post.objects.filter(is_active=True)[:4]

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
        'selected_category': category_id,
        'query': query,
    }
    return render(request, 'blog.html', context)


def blog_details(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_active=True)
    post.increment_views()

    categories = Category.objects.all()
    recent_posts = Post.objects.filter(is_active=True).exclude(id=post_id)[:4]
    prev_post = Post.objects.filter(is_active=True, id__lt=post_id).order_by('-id').first()
    next_post = Post.objects.filter(is_active=True, id__gt=post_id).order_by('id').first()
    comments = post.get_approved_comments()

    context = {
        'post': post,
        'categories': categories,
        'recent_posts': recent_posts,
        'prev_post': prev_post,
        'next_post': next_post,
        'comments': comments,
    }
    return render(request, 'blog_details.html', context)


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id, is_active=True)
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')

        if not content:
            return JsonResponse({'status': 'error', 'message': 'Comment cannot be empty.'})

        parent = None
        if parent_id:
            if not request.user.is_staff:
                return JsonResponse({'status': 'error', 'message': 'Only admins can reply to comments.'})
            try:
                parent = Comment.objects.get(id=parent_id, post=post, is_approved=True)
            except Comment.DoesNotExist:
                pass

        # Admin comments are auto-approved
        is_approved = request.user.is_staff
        Comment.objects.create(
            post=post,
            author=request.user,
            parent=parent,
            content=content,
            is_approved=is_approved,
        )
        if is_approved:
            message = 'Your comment has been posted.'
        else:
            message = 'Your comment has been submitted and is awaiting approval.'
        return JsonResponse({'status': 'success', 'message': message})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
