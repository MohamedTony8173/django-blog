import os

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from PIL import Image


def validate_image(file):
    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        raise ValidationError("Invalid image file!")

    valid_formats = ["JPEG", "PNG"]
    if img.format not in valid_formats:
        raise ValidationError("Only JPG and PNG images are allowed.")


class UserManager(BaseUserManager):
    def create_superuser(self, email, username, password=None, **extra):
        extra.setdefault("is_active", True)
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)

        if extra.get("is_active") is not True:
            raise ValueError("active must be true")
        if extra.get("is_staff") is not True:
            raise ValueError("staff must be true")
        if extra.get("is_superuser") is not True:
            raise ValueError("superuser must be true")

        email = self.normalize_email(email)
        user = self.create_user(email, username, password, **extra)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password=None, **extra):
        email = self.normalize_email(email)
        if not email:
            raise ValueError("email is required")
        user = self.model(email=email, username=username, password=None, **extra)
        user.set_password(password)
        user.save()
        return user


class UserCustom(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=225, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(UserCustom, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to="profile/", validators=[validate_image], default="user.png"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            old_image = UserProfile.objects.get(pk=self.pk).photo
        except UserProfile.DoesNotExist:
            old_image = None
        super().save(*args, **kwargs)
        # If new image is uploaded and it's different → delete the old file
        if old_image and old_image != self.photo:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)


        

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=UserCustom)
def user_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        group = Group.objects.get(name="Regular User")
        instance.groups.add(group)


@receiver(post_delete, sender=UserProfile)
def delete_userprofile_photo(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(save=False)

