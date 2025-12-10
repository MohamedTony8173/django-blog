from django.contrib import admin
from .models import Category, Blog , Comment


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "blog_title",
        "blog_author",
        "blog_category__category_name",
        "blog_status",
        "is_feature",
    )

    search_fields = (
        "blog_title",
        "blog_author",
        "blog_category__category_name",
        "blog_status",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {"blog_slug": ["blog_title"]}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "created_at", "updated_at")
    prepopulated_fields = {"category_slug": ["category_name"]}
    search_fields = ("category_name",)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)

