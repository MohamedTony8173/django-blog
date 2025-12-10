from django.db import models


class About(models.Model):
    about_header = models.CharField(max_length=200)
    about_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.about_header


class SocialLink(models.Model):
    social_name = models.CharField(max_length=100)
    social_icon = models.ImageField(upload_to="icon/")
    social_link = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.social_name
