from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = "women/index.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")

        # Объединение данных
        for key, val in c_def.items():
            context[key] = val
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related("cat")


# def index(request):
#     context = {"title": "Главная страница",
#                "cats": cats,
#                "cat_selected": "vse-kategorii",
#                "posts": posts}
#     posts = Women.objects.all()
#     cats = Category.objects.all()
#     context = {"title": "Главная страница",
#                "cats": cats,
#                "cat_selected": "vse-kategorii",
#                "posts": posts}
#     return render(request, "women/index.html", context=context)


def about(request):
    context_list = Women.objects.all()
    paginator = Paginator(context_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"title": "О сайте",
               "menu": menu,
               "page_obj": page_obj}
    return render(request, "women/about.html", context=context)


# def add_page(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             try:
#                 form.save()
#                 return redirect("home")
#
#             except:
#                 form.add_error(None, "Ошибка добавления поста")
#     else:
#         form = AddPostForm()
#     return render(request, "women/add_page.html",
#                   context={"title": "Добавление Статьи", "form": form})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/add_page.html"
    # Редирект после добавления поста (нажатия кнопки "Добавить") (ниже)
    success_url = reverse_lazy("home")
    # login_url Указывает страницу перенаправления для неавторизированного пользователя
    login_url = reverse_lazy("home")

    # raise_exception порождает ошибку 403 - доступ запрещён
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")

        # Объединение данных
        for key, val in c_def.items():
            context[key] = val
        return context


def just_info(request):
    return redirect('contact')


# def contact(request):
#     return render(request, "women/contact.html", context={'title': "Обратная связь"})


# def login(request):
#     return render(request, "women/login.html", context={"title": "Авторизация"})


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    context = {"title": post.title,  # ТУТ БЫЛО 'menu': menu,
               "post": post,
               "cat_selected": post.cat_id}
    return render(request, "women/post.html", context=context)


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"  # Имя аргумента, который берётся из urls.py как <slug:post_slug>.
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["post"])

        # Обработка данных
        for key, val in c_def.items():
            context[key] = val
        return context


class ContactFormView(DataMixin, FormView):  # FormView - стандартный класс, не привязанный к модели.
    form_class = ContactForm
    template_name = "women/contact.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")

        # Обработка данных
        for key, val in c_def.items():
            context[key] = val
        return context

    def form_valid(self, form):
        """ Действия, происходящие при корректном заполнении формы """
        # form.cleaned_data - словарь, содержащий все данные, заполненные пользователем в форме.
        print(form.cleaned_data)
        return redirect("home")


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs["cat_slug"],
                                    is_published=True).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Категория - " + str(context["posts"][0].cat)
        context["menu"] = menu
        context["cat_selected"] = context["posts"][0].cat_id
        c = Category.objects.get(slug=self.kwargs["cat_slug"])
        c_def = self.get_user_context(title="Категория - " + str(c.name),
                                      cat_selected=c.pk)
        # Обработка данных
        for key, val in c_def.items():
            context[key] = val
        return context


# def show_category(request, cat_slug):
#     to_cat_id = {"aktrisy": 1, "pevicy": 2}  # СПОСОБ ХУЙНЯ СПОСОБ ХУЙНЯ СПОСОБ ХУЙНЯ
#     posts = Women.objects.filter(cat_id=to_cat_id[cat_slug])
#     cats = Category.objects.all()

# if len(posts) == 0:
#     raise Http404()
# context = {"title": "Посты по категориям",
#            "cat_selected": cat_slug,
#            "posts": posts}
# return render(request, "women/index.html", context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class RegisterUser(DataMixin, CreateView):  # CreateView - для работы с базой данных подходит
    form_class = RegisterUserForm  # Наша пользовательская Форма для заполнения обычным пользователем
    template_name = "women/register.html"  # Имя шаблона, куда будут передаваться все данные
    success_url = reverse_lazy("login")  # Что делать при успешном выполнении регистрации

    # (хз как работает, но как то request.GET возвращает значение о выполнении формы вроде)

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Передатчик всех данных в шаблон указанный в template_name """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")  # Какая-то пользовательская залупка

        # Обработка данных
        for key, val in c_def.items():
            context[key] = val
        return context

    def form_valid(self, form):
        """ Действия, происходящие при успешной регистрации пользователя """
        user = form.save()  # Добавление пользователя в бд аккаунтов сайта.
        login(self.request, user)  # Автоматическая авторизация.
        return redirect("home")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm  # Встроенная форма
    template_name = "women/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Передатчик всех данных в шаблон указанный в template_name """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")  # Какая-то пользовательская залупка

        # Обработка данных
        for key, val in c_def.items():
            context[key] = val
        return context

    def get_success_url(self):
        """ Действия, происходящие при успешной авторизации """
        return reverse_lazy("home")


def logout_user(request):
    """ обработчик выхода из аккаунта """
    logout(request)
    return redirect("login")
