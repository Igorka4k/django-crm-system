from django.db.models import Count

from .models import *

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"}]


class DataMixin:
    paginate_by = 30

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count("women"))
        # к каждому объекту категорий будет добавлен аттрибут кол-ва записей в таблице Women,
        # относящиеся к этой категории women__count

        # Скрываем раздел добавления статьи для неавторизованного пользователя
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context["menu"] = user_menu
        context["cats"] = cats
        if "cat_selected" not in context:
            context["cat_selected"] = 0
        return context
