from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="логин", widget=forms.TextInput(attrs={'class': 'login-page__form-input-box'}))
    password = forms.CharField(label="пароль", widget=forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="логин")
    password1 = forms.CharField(label="пароль", widget=forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}))
    password2 = forms.CharField(label="повтор пароля", widget=forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}))


    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widget = {
            'email': forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}),
            'first_name': forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}),
            'last_name': forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}),
        }



    # def cleen_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['passworfd2']:
    #         raise forms.ValidationError('Пароли не совпадают')
    #     return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой e-mail уже зареген!')
        return email



class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="логин", widget=forms.TextInput(attrs={'class': 'login-page__form-input-box'}))
    email = forms.CharField(disabled=True, label="E-mail", widget=forms.TextInput(attrs={'class': 'login-page__form-input-box'}))


    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widget = {
            'first_name': forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}),
            'last_name': forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}))
    new_password2 = forms.CharField(label="Новый пароль повтор", widget=forms.PasswordInput(attrs={'class': 'login-page__form-input-box'}))
