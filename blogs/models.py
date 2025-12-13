from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from PIL import Image
from django.urls import reverse
import os

User = get_user_model()


def validate_image(file):
    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        raise ValidationError("Invalid image file!")

    valid_formats = ["JPEG", "PNG"]
    if img.format not in valid_formats:
        raise ValidationError("Only JPG and PNG images are allowed.")


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_slug = models.SlugField(max_length=120, unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("-created_at",)


BLOG_STATUS = (
    ("draft", "draft"),
    ("published", "published"),
)


class Blog(models.Model):
    blog_title = models.CharField(max_length=225, unique=True)
    blog_slug = models.SlugField(max_length=255, unique=True)
    blog_author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    blog_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blog_feature_image = models.ImageField(
        upload_to="blogs/%Y%m", validators=[validate_image], default="blog.png"
    )
    blog_short_description = models.CharField(max_length=400)
    blog_long_description = models.TextField()
    blog_status = models.CharField(max_length=10, choices=BLOG_STATUS, default="draft")
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            old_image = Blog.objects.get(pk=self.pk).blog_feature_image
        except Blog.DoesNotExist:
            old_image = None

        super().save(*args, **kwargs)

        # If new image is uploaded and it's different → delete the old file
        if old_image and old_image != self.blog_feature_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)

    def __str__(self):
        return self.blog_title

    def get_absolute_url(self):
        return reverse("blogs:blog_single", kwargs={"slug": self.blog_slug})

    class Meta:
        ordering = ("-created_at",)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.blog.blog_title}"
