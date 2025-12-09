from django.shortcuts import get_object_or_404, render
from .models import Blog,Category
from django.db.models import Q

def home(request):
    blogs_feature = Blog.objects.filter(is_feature=True,blog_status='published').order_by('?').first()
    blogs_features = Blog.objects.filter(is_feature=True,blog_status='published').order_by('?')[:2]
    all_blog = Blog.objects.filter(blog_status='published').exclude(is_feature=True).order_by('?')[:4]
    context = {
        'blogs_feature':blogs_feature,
        'blogs_features':blogs_features,
        'all_blog':all_blog
    }
    return render(request,'blogs/index.html',context)


def blog_by_category(request,slug):
    category = get_object_or_404(Category,category_slug=slug) 
    blogs = Blog.objects.filter(blog_status='published',blog_category=category)
    context = {
        'category':category,
        'blogs':blogs
    }
    return render(request,'blogs/blog_cat.html',context)


def blog_single(request,slug):
    blog = get_object_or_404(Blog,blog_slug=slug)
    context = {
        'blog':blog
    }
    return render(request,'blogs/blog_single.html',context)


def blog_search(request):
    keyword = request.GET.get('keyword','').strip()
    result =[]
    if keyword:
        result = Blog.objects.filter(Q(blog_title__icontains=keyword) | Q(blog_author__username__icontains=keyword) )
    context = {
        'keyword':keyword,
        'result':result
    }    
    return render(request,'blogs/blog_search.html',context)    