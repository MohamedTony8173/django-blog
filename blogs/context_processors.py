from .models import Category


def categories_list(request):
    return {"categories": Category.objects.all()}
