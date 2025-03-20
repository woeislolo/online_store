from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Адрес')
    post_code = forms.CharField(label='Индекс')
    city = forms.CharField(label='Город')

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'post_code', 'city']
        