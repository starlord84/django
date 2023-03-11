from django.db.models import Count, F
from News.models import Category
from django import template
from django.core.cache import cache
register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('News/list_categories.html')
def show_categories(arg1='Список', arg2='категорий'):
    # categories = Category.objects.all()
    # categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
        cache.set('categories', categories, 60)
    return {'categories': categories, 'arg1': arg1, 'arg2': arg2}
