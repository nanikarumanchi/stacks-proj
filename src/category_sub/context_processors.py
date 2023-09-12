from .models import Category


def category_list(request):
    qs = Category.objects.all()
    context = {
        'cat_list': qs
    }
    return context
