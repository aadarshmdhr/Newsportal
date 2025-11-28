from newspaper.models import Category


def navigation(request):
    categories = Category.objects.all()[:5]
    return {"categories": categories}