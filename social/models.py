from django.db import models
from django.db.models.signals import pre_save,post_delete
from django.dispatch import receiver
import os

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


@receiver(pre_save, sender=SocialLink)
def delete_old_social_icon(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if it's a new object

    try:
        old_file = SocialLink.objects.get(pk=instance.pk).social_icon
    except SocialLink.DoesNotExist:
        return

    new_file = instance.social_icon
    if old_file and old_file != new_file:
        old_file.delete(save=False)  # safer than os.remove



@receiver(post_delete, sender=SocialLink)
def delete_social_icon_on_delete(sender, instance, **kwargs):
    if instance.social_icon:
        instance.social_icon.delete(save=False)


