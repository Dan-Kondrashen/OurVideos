from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import PasswordInput, ModelForm
from django.core.validators import validate_email
from .models import UserInfo, Comments

from mySite.models import Videos, VideoType, VideoDirector, Rating, RatingStar, VideoCountrу

video = Videos.objects.all()
typeV = VideoType.objects.all()


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username')
    password = forms.CharField(required=True, label='Пароль')


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(min_length=3, max_length=10, required=True, label='Никнейм', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Может содержать только латинские буквы и цифры',
            code='invalid_username'
        ),
    ])

    email = forms.CharField(min_length=3, required=True, label='Email')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        # валидация паролей

        # валидация никнейма
        username = self.cleaned_data.get("username")
        # валидация паролей
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                {'password_confirm': "Пароли не совпадают", 'password': ''}
            )

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError({'username': "Такой логин уже занят"})

        # валидация email
        try:
            validate_email(self.cleaned_data.get("email"))
        except ValidationError as e:
            raise forms.ValidationError({'email': "Email не является валидным адресом"})

        return cleaned_data


class ChoiseForm(forms.Form):
    types = forms.ModelChoiceField(VideoType.objects.all(), label="Выберите 1-ый жанр", required=False)
    types1 = forms.ModelChoiceField(VideoType.objects.all(), label="Выберите 2-ой жанр", required=False)
    videos = forms.ModelChoiceField(VideoDirector.objects.all(), label="Выберите режисера ", required=False)
    vids = forms.ModelChoiceField(VideoCountrу.objects.all(), label="Выберите страну ", required=False)


class userChangeInfo(forms.Form):
    user = forms.CharField(min_length=3, max_length=10, required=True, label='Никнейм', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Может содержать только латинские буквы и цифры',
            code='invalid_username'
        ),
    ])
    emailF = forms.CharField(min_length=3, required=True, label='Email')


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']


class SearchForm(forms.Form):
    searchText = forms.CharField(min_length=3, required=True)


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ['star']
