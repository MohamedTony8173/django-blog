from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from blogs.models import Blog, Category, Comment
from users.models import UserProfile

from .forms import (BlogForm, CategoryForm, DashboardUserForm,
                    DashboardUserFormCreation, DashboardUserProfile)

User = get_user_model()

@login_required
def dashboard(request):
    # Group blogs by category & count them
    category_counts = Blog.objects.values("blog_category__category_name").annotate(
        total=Count("id")
    )
    blogs = Blog.objects.filter(blog_status='published').count()
    labels = [item["blog_category__category_name"] for item in category_counts]
    data = [item["total"] for item in category_counts]

    context = {
        "labels": labels,
        "data": data,
        'blogs':blogs
    }
    return render(request, "dashboards/index.html", context)

@login_required
def dashboard_blogs(request):
    blogs = Blog.objects.all()
    context = {"blogs": blogs}
    return render(request, "dashboards/blogs/blogs.html", context)

@login_required
def dashboard_edit_blog(request, slug):
    blog = get_object_or_404(Blog, blog_slug=slug)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Post Was Updated Successfully!")
            return redirect("dashboards:dashboard_blogs")
        else:
            messages.error(
                request,
                "Post Was Not Updated? Please Check Your Input Fields and Type Correct Information",
            )
            return redirect(request.path_info)

    else:
        form = BlogForm(instance=blog)
    context = {"form": form, "blog": blog}
    return render(request, "dashboards/blogs/blog_edit.html", context)

@login_required
def dashboard_blog_delete(request, slug):
    blog = get_object_or_404(Blog, blog_slug=slug)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Post Was Deleted Successfully!")
        return redirect("dashboards:dashboard_blogs")

    context = {"blog": blog}
    return render(request, "dashboards/blogs/blog_delete.html", context)

@login_required
def dashboard_blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["blog_title"]
            f = form.save(commit=False)
            f.blog_author = request.user
            f.blog_slug = slugify(title)
            f.save()
            messages.success(request, "Post Was Created Successfully!")
            return redirect("dashboards:dashboard_blogs")
    else:
        form = BlogForm()
    return render(request, "dashboards/blogs/blog_create.html", {"form": form})

@login_required
def dashboard_categories(request):
    return render(request, "dashboards/categories/categories.html")

@login_required
def dashboard_category_edit(request, slug):
    category = get_object_or_404(Category, category_slug=slug)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            cat_name = form.cleaned_data["category_name"]
            f = form.save(commit=False)
            f.category_slug = slugify(cat_name)
            f.save()
            messages.success(request, "Edit Category Successfully!")
            return redirect("dashboards:dashboard_categories")
    else:
        form = CategoryForm(instance=category)
    context = {"form": form, "category": category}

    return render(request, "dashboards/categories/category_edit.html", context)

@login_required
def dashboard_category_delete(request, slug):
    category = get_object_or_404(Category, category_slug=slug)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Deleted Category Successfully!")
        return redirect("dashboards:dashboard_categories")
    context = {"category": category}
    return render(request, "dashboards/categories/category_delete.html", context)

@login_required
def dashboard_category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["category_name"]
            f = form.save(commit=False)
            f.author = request.user
            f.category_slug = slugify(name)
            f.save()
            messages.success(request, "Created Category Successfully!")
            return redirect("dashboards:dashboard_categories")
    else:
        form = CategoryForm(request.POST)
    return render(request, "dashboards/categories/category_create.html", {"form": form})

@login_required
def dashboard_user(request):
    users = User.objects.all().exclude(is_superuser=True)
    return render(request, "dashboards/users/index.html", {"users": users})

@login_required
def dashboard_user_edit(request, username):
    user = get_object_or_404(User, username=username)
    user_pro = get_object_or_404(UserProfile, user=user)
    if request.method == "POST":
        form = DashboardUserForm(request.POST, instance=user)
        pro_form = DashboardUserProfile(request.POST, request.FILES, instance=user_pro)
        if form.is_valid() and pro_form.is_valid():
            form.save()
            pro_form.save()
            messages.success(request, "User Updated Successfully!")
            return redirect("dashboards:dashboard_user")
        else:
            messages.error(
                request, "User Not Updated! Please be Sure with Your Data Inserted"
            )
            return redirect(request.path_info)
    else:
        form = DashboardUserForm(instance=user)
        pro_form = DashboardUserProfile(instance=user_pro)
    context = {"form": form, "user": user, "pro_form": pro_form}
    return render(request, "dashboards/users/user_edit.html", context)

@login_required
def dashboard_user_delete(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        user.delete()
        messages.success(request, "Deleted User Successfully!")
        return redirect("dashboards:dashboard_user")
    context = {"user": user}
    return render(request, "dashboards/users/user_delete.html", context)

@login_required
def dashboard_user_create(request):
    if request.method == "POST":
        form = DashboardUserFormCreation(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Created Successfully!")
            return redirect("dashboards:dashboard_user")
        else:
            messages.error(
                request, "User Not Updated! Please be Sure with Your Data Inserted"
            )
            return redirect(request.path_info)
    else:
        form = DashboardUserFormCreation(request.POST)
    context = {
        "form": form,
    }
    return render(request, "dashboards/users/user_create.html", context)



@login_required
def dashboard_comments(request):
    comments = Comment.objects.all()
    context = {
        'comments':comments
    }
    return render(request, "dashboards/comments/index.html", context)

@login_required
def dashboard_comments_delete(request,comment):
    comment = get_object_or_404(Comment,pk=comment)
    if request.method == 'POST':
        comment.delete()
        messages.success(request,'it was deleted!')
        return redirect('dashboards:dashboard_comments')
    context = {
        'comment':comment
    }
    return render(request, "dashboards/comments/comment_delete.html", context)

@login_required
def dashboard_comments_show(request,comment):
    comment = get_object_or_404(Comment,pk=comment)
    context = {
        'comment':comment
    }
    return render(request, "dashboards/comments/comment_show.html", context)


@login_required
def dashboard_comments_search(request):
    key = request.GET.get('keyword','')
    if key:
        comments = Comment.objects.filter(user__username__icontains=key)
    context = {
        'comments':comments
    }
    return render(request, "dashboards/comments/search.html", context)


@login_required
def user_profile(request):
    user = request.user
    user_pro = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST':
        form = DashboardUserProfile(request.POST,request.FILES,instance=user_pro)
        if form.is_valid():
            form.save()
            messages.success(request,'it was Updated!')
            return redirect(request.path_info)
    else:
        form = DashboardUserProfile(instance=user_pro)  
    context = {
        'form':form,
        'user_pro':user_pro
    }
    return render(request, "dashboards/users/profile.html", context)      

    