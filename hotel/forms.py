from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Room, RoomCategory, Order, Client, ClientUser


class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('number',
                  'type')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = RoomCategory
        fields = ('category_name',
                  'price_per_day',
                  'persons',
                  'image',
                  'desc')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'first_name',
            'patronymic',
            'last_name',
            'country',
            'passport',
            'birthday',
            'gender')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'entry_date',
            'departure_date',)


class VisitorForm(forms.ModelForm):
    class Meta:
        model = ClientUser
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'phone'
        )


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):

    email = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    patronymic = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Эл. почта'
        self.fields['username'].label = 'Логин'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['first_name'].label = 'Имя'
        self.fields['patronymic'].label = 'Отчество'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный электронный адрес уже зарегистрирован')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Данный логин уже используется')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'phone', 'password', 'confirm_password')


class StaffForm(forms.ModelForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    patronymic = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    position = forms.CharField(required=True)
    salary = forms.IntegerField(required=True)
    passport = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    username = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['first_name'].label = 'Имя'
        self.fields['patronymic'].label = 'Отчество'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['position'].label = 'Должность'
        self.fields['salary'].label = 'Зарплата'
        self.fields['passport'].label = 'Паспортные данные'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Данный логин уже используется')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'patronymic',
                  'phone',
                  'position',
                  'salary',
                  'passport',
                  'username',
                  'password',
                  'confirm_password')
