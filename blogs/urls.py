from django.urls import path
from . import views

app_name = "blogs"

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>/", views.blog_by_category, name="blog_by_category"),
    path("blogs/<slug:slug>/", views.blog_single, name="blog_single"),
    path("search/", views.blog_search, name="search"),
]
