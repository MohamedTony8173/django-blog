from .models import Category
from social.models import About, SocialLink


def categories_list(request):
    return {"categories": Category.objects.all()}


def social_about(request):
    return {"about": About.objects.first()}


def social_link(request):
    return {"social_links": SocialLink.objects.all()}
