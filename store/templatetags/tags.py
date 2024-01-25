from django import template

from store.models import Category

register = template.Library()


@register.simple_tag()
def tag_cetegory():
    return Category.objects.all()
