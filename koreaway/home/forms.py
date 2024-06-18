from django import forms

from home.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'phone']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'address': 'Адрес',
            'phone': 'Телефон',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Введите вашу фамилию'}),
            'address': forms.TextInput(attrs={'placeholder': 'Введите ваш адрес'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Введите ваш телефон'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Ваше имя',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
            }
        )
    )
    email = forms.EmailField(
        label='Ваша почта',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ваша почта',
            }
        )
    )
    message = forms.CharField(
        label='Ваше сообщение',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ваше сообщение',
                'rows': 5,
            }
        )
    )
