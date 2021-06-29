from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Категория не выбрана"

    class Meta:
        model = Women
        fields = ["title", "slug", "content", "photo", "is_published", "cat"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 60, "rows": 10})
        }

    def clean_title(self):
        """ Пользовальский валидатор"""
        title = self.cleaned_data["title"]
        if len(title) > 200:
            raise ValidationError("Длина превышает 200 символов")
        return title


class RegisterUserForm(UserCreationForm):
    """ Логика регистрации пользователя """

    # Так как подключение стилей через widgets в классе Meta работает каряво, пропишем
    # оформление полей через CharField как отдельные аттрибуты RegisterUserForm.
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.CharField(label="Email",
                            widget=forms.EmailInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(label="Повтор пароля",
                                widget=forms.PasswordInput(attrs={"class": "form-input"}))

    class Meta:
        model = User  # Встроенная стандартная модель, которая работает с таблицей auth_user
        fields = ("username", "email", "password1", "password2")  # Поля, которые будут отображаться

        # Оформление для отображения полей fields
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-input"}),
            # "email": forms.EmailInput(attrs={"class": "form-input"}),
            "password1": forms.PasswordInput(attrs={'class': "form-input"}),
            "password2": forms.PasswordInput(attrs={"class": "form-input"})
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 60, "rows": 10}))
    captcha = CaptchaField()
