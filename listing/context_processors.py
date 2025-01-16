from .models import Category, SubCategory

def categories_processor(request):
    return {
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
    }