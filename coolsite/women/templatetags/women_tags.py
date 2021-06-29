from django import template
from women.models import *

register = template.Library()


# @register.simple_tag(
#     name="getcats")  # name="<имя>" - имя по которому надо будет обращаться к тегу в шаблоне.
# def get_categories(cat_id=None):
#     if not cat_id:
#         return Category.objects.all()
#     return Category.objects.filter(pk=cat_id)


@register.inclusion_tag("women/my_user_tags/list_categories.html")
def show_categories(sort=None, cat_selected="vse_kategorii"):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "sort": sort, "cat_selected": cat_selected}


@register.inclusion_tag("women/my_user_tags/main_menu_list.html")
def show_main_menu():
    menu = [
        {"title": "О сайте", "url_name": "about"},
        {"title": "Добавить статью", "url_name": "add_page"},
        {"title": "Обратная связь", "url_name": "contact"},
        {"title": "WITH USER TAG", "url_name": "just_info"},
        {"title": "Войти", "url_name": "login"}]
    return {"menu": menu}
