from django.shortcuts import get_object_or_404, render, redirect
from .models import Blog, Category, Comment
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    blogs_feature = (
        Blog.objects.filter(is_feature=True, blog_status="published")
        .order_by("?")
        .first()
    )
    blogs_features = Blog.objects.filter(
        is_feature=True, blog_status="published"
    ).order_by("?")[:2]
    all_blog = (
        Blog.objects.filter(blog_status="published")
        .exclude(is_feature=True)
        .order_by("?")[:4]
    )
    context = {
        "blogs_feature": blogs_feature,
        "blogs_features": blogs_features,
        "all_blog": all_blog,
    }
    return render(request, "blogs/index.html", context)


def blog_by_category(request, slug):
    category = get_object_or_404(Category, category_slug=slug)
    blogs = Blog.objects.filter(blog_status="published", blog_category=category)
    context = {"category": category, "blogs": blogs}
    return render(request, "blogs/blog_cat.html", context)


def blog_single(request, slug):
    blog = get_object_or_404(Blog, blog_slug=slug)
    comments_count = Comment.objects.filter(blog__blog_slug=slug)
    context = {"blog": blog, "comments_count": comments_count}
    return render(request, "blogs/blog_single.html", context)


def blog_search(request):
    keyword = request.GET.get("keyword", "").strip()
    result = []
    if keyword:
        result = Blog.objects.filter(
            Q(blog_title__icontains=keyword)
            | Q(blog_author__username__icontains=keyword)
        )
    context = {"keyword": keyword, "result": result}
    return render(request, "blogs/blog_search.html", context)


def write_comment(request, b_slug):
    blog = get_object_or_404(Blog, blog_slug=b_slug)
    comments_user = Comment.objects.filter(
        blog__blog_slug=b_slug, user=request.user
    ).exists()

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to comment.")
        return redirect("users:login")
    if request.method == "POST":
        if comments_user:
            messages.error(request, "You Already Comments this Blog")
            return redirect("blogs:blog_single", slug=b_slug)
        if len(request.POST["comment"]) <= 0:
            messages.error(request, "You must type character to comment.")
            return redirect("blogs:blog_single", slug=b_slug)
        else:
            Comment.objects.create(
                blog=blog, user=request.user, body=request.POST.get("comment")
            )
            messages.success(request, "Comment was created successfully!")

    return redirect("blogs:blog_single", slug=b_slug)
