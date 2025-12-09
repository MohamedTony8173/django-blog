from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from PIL import Image
from django.urls import reverse

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "categories"


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

    def __str__(self):
        return self.blog_title


    def get_absolute_url(self):
        return reverse('blogs:blog_single', kwargs={'slug': self.blog_slug})