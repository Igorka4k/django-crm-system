from django.contrib import admin

from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "time_create", "photo", "is_published")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "time_create")
    fields = ("title", "slug", "cat", "content", "photo", "get_html_photo", "is_published",
              "time_create", "time_update")
    readonly_fields = ("time_create", "time_update", "get_html_photo")
    prepopulated_fields = {"slug": ("title",)}  # авто-заполнение поля slug на основе поля title
    save_on_top = True  # Отображать повторно панель управления сверху при редактировании записей.

    def get_html_photo(self, object):  # object ссылается на объект класса-модели Women.
        """ Вставка миниатюры фотографии во все таблицы админки """
        # Метод может называться произвольно и вызывается только когда надо.
        # функция mark_safe указывает не экранировать теги.

        if object.photo:  # не у всех тёлок есть img.
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра фото"  # шорт_дескрипшн хуй


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}  # авто-заполнение поля slug на основе поля name


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
