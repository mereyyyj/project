from django.shortcuts import render, redirect
from django.contrib.auth import login
import google.generativeai as genai
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Catalog
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order
from .forms import CalorieCalculatorForm

load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")

genai.configure(api_key=GENAI_API_KEY)


def chat_bot(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        if not user_message:
            return JsonResponse({"response": "Введите сообщение!"})

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_message)

        print(response.text)  # Проверяем, что API вернул ответ

        return JsonResponse({"response": response.text}) if hasattr(response, "text") else JsonResponse({"response": "Ошибка API!"}, status=500)

    return JsonResponse({"response": "Используйте POST-запрос!"}, status=405)

def sign_up(request):
    if request.method == 'POST':
        print(request.POST)
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.bio = form.cleaned_data.get('bio', '')
            user.profile_picture = form.cleaned_data.get('profile_picture')
            user.save()
            login(request, user)
            return redirect('profile')
        else:
            print(form.errors)  # Логирование ошибок

    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/sign_up.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Перенаправление на профиль
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/log_in.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect('profile')
        else:
            messages.error(request, "Ошибка при обновлении профиля.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'main/profile.html', {'form': form})



def index(request):
    catalogs = Catalog.objects.all().order_by('-date_added')  # можно менять сортировку
    return render(request, 'main/index.html', {'catalogs': catalogs})


def about(request):
    return render(request, 'main/about.html')

def chat_page(request):
    return render(request, "chat_bot/chat_bot.html")

def gp_helper_view(request):
    return render(request, 'chat_bot/gp_helper.html')

def chat_combined(request):
    return render(request, 'chat_bot/chat_combined.html')





@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        cart, created = CartItem.objects.get_or_create(
            user=request.user,
            product_id=product_id,
            defaults={'quantity': 1}
        )
        if not created:
            cart.quantity += 1
            cart.save()

        messages.success(request, "Товар добавлен в корзину")
        return redirect('basket')

    return redirect('catalog')


@login_required
def basket(request):
    items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_subtotal() for item in items)
    return render(request, 'main/basket.html', {'items': items, 'total_price': total_price})

@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_subtotal() for item in items)

    return render(request, 'main/checkout.html', {
        'items': items,
        'total_price': total_price
    })

@login_required
def clear_basket(request):
    CartItem.objects.filter(user=request.user).delete()
    messages.info(request, "Корзина очищена")
    return redirect('basket')

@login_required
def process_payment(request):
    if request.method == "POST":
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, "Оплата прошла успешно!")
        return redirect('catalog')
    return redirect('checkout')



@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_subtotal() for item in cart_items)

    if request.method == "POST":
        # Сохраняем заказ
        Order.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            card_number=request.POST['card_number'],
            expiration_date=request.POST['expiration_date'],
            cvv=request.POST['cvv'],
            total_price=total_price
        )
        cart_items.delete()
        return render(request, 'main/checkout.html', {
            'success': True,
            'cart_items': [],
            'total_price': 0,
        })

    return render(request, 'main/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })



def survey(request):
        if request.method == 'POST':
            form = CalorieCalculatorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('chat_combined')  # или поменяй на другую страницу по желанию
        else:
            form = CalorieCalculatorForm()
        return render(request, 'main/survey.html', {'form': form})





