from django.urls import path
from . import views

app_name = "dashboards"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("blogs/", views.dashboard_blogs, name="dashboard_blogs"),
    path(
        "blogs/edit/<slug:slug>/", views.dashboard_edit_blog, name="dashboard_edit_blog"
    ),
    path(
        "blogs/delete/<slug:slug>/",
        views.dashboard_blog_delete,
        name="dashboard_delete_blog",
    ),
    path("blogs/create/", views.dashboard_blog_create, name="dashboard_blog_create"),

    # categories
    path("categories/", views.dashboard_categories, name="dashboard_categories"),
    path(
        "categories/edit/<slug:slug>/",
        views.dashboard_category_edit,
        name="category_edit",
    ),
    path(
        "categories/delete/<slug:slug>/",
        views.dashboard_category_delete,
        name="category_delete",
    ),
    path(
        "categories/create/",
        views.dashboard_category_create,
        name="dashboard_category_create",
    ),

    # comments
    path('comments/',views.dashboard_comments,name='dashboard_comments'),
    path('comments/<str:comment>/delete/',views.dashboard_comments_delete,name='dashboard_comments_delete'),
    path('comments/<str:comment>/show/',views.dashboard_comments_show,name='dashboard_comments_show'),
    path('comments/search/',views.dashboard_comments_search,name='dashboard_comments_search'),
    # users

    path('users/',views.dashboard_user,name='dashboard_user'),
    path('users/create/',views.dashboard_user_create,name='dashboard_user_create'),
    path('users/<str:username>/edit/',views.dashboard_user_edit,name='dashboard_user_edit'),
    path('users/<str:username>/delete/',views.dashboard_user_delete,name='dashboard_user_delete'),

    # user profile
      # profile user
    path('profile/',views.user_profile,name='user_profile')
]
