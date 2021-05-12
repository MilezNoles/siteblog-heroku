from django import forms
from .models import *  # для выпадающего списка категорий
import re  # для clean_title
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.text import slugify

# from captcha.fields import CaptchaField


class UserLogin(AuthenticationForm):
    username = forms.CharField(label="Login",
                               widget=forms.TextInput(attrs={'class': "form-control",
                                                             "placeholder": "Username or Email"}), )
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': "form-control", }))


class UserRegister(UserCreationForm):
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={'class': "form-control", }),
                               help_text="Mast be less than 150 chars")
    email = forms.EmailField(label="Email",
                             help_text="You will receive message with your register details",
                             widget=forms.EmailInput(attrs={'class': "form-control", }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': "form-control", }),
                                help_text="Longer than 8 chars (letters & nums)")
    password2 = forms.CharField(label="Confirm password",
                                widget=forms.PasswordInput(attrs={'class': "form-control", }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email has been already used!")
        return email


    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        # widgets = {"username" : forms.TextInput(attrs={'class': "form-control", }),
        #            "email": forms.EmailInput(attrs={'class': "form-control", }),
        #            "password1" : forms.PasswordInput(attrs={'class': "form-control", }),
        #            "password2": forms.PasswordInput(attrs={'class': "form-control", }),
        #
        # } для UserCreationForm это поле работает не корректно, поэтому все переносим из меты в UserRegister

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "city","occupation", "profile_picture","send_email" ]
        widgets = {"bio" : forms.Textarea(attrs={'class': "form-control", }),
                   "city": forms.TextInput(attrs={'class': "form-control","placeholder":"это поле обязательно для сервиса поиска", }),
                   "occupation": forms.TextInput(attrs={'class': "form-control","placeholder":"это поле обязательно для сервиса поиска", }),
                   "send_email": forms.CheckboxInput(attrs={'class': "form-check-input",}),
                   "profile_picture": forms.FileInput(attrs={'class': "form-control",}),

        }



class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["username", "comment",]
        widgets = {
            "username": forms.TextInput(attrs={'class': "name", "type": "hidden" }, ),      # "type": "hidden"
            "comment": forms.TextInput(attrs={
                "placeholder": "Comment",
                'class': "comment",
            }),

        }


    # def clean_username(self):  # валидатор для title пример
    #     username = self.cleaned_data["username"]
    #     if re.match(r"\d", username):  # \d цифра
    #         raise ValidationError("Ник не должен начинаться с цифры")
    #     return username
