from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CalorieCalculatorResponse

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")



class ProfileUpdateForm(forms.ModelForm):
    location = forms.CharField(max_length=100, required=False, label='Локация')

    class Meta:
        model = User
        fields = ('profile_picture', 'location')

class PaymentForm(forms.Form):
    full_name = forms.CharField(label='ФИО', max_length=100)
    card_number = forms.CharField(label='Номер карты', max_length=20)
    expiration_date = forms.CharField(label='Срок действия (MM/YY)', max_length=5)
    cvv = forms.CharField(label='CVV', max_length=4, widget=forms.PasswordInput)



class CalorieCalculatorForm(forms.ModelForm):
    class Meta:
        model = CalorieCalculatorResponse
        fields = ['full_name', 'age', 'gender', 'height', 'weight', 'activity_level', 'goal']
        labels = {
            'full_name': 'Имя',
            'age': 'Возраст',
            'gender': 'Пол',
            'height': 'Рост (см)',
            'weight': 'Вес (кг)',
            'activity_level': 'Уровень физической активности',
            'goal': 'Цель',
        }
        widgets = {
            'gender': forms.RadioSelect,
            'activity_level': forms.RadioSelect,
            'goal': forms.RadioSelect,
        }
