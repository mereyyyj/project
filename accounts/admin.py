from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Catalog
from .models import CalorieCalculatorResponse
from .models import CartItem, Order

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active')

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Catalog)

@admin.register(CalorieCalculatorResponse)
class CalorieCalculatorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'gender', 'height', 'weight', 'activity_level', 'goal', 'submitted_at')
    list_filter = ('gender', 'activity_level', 'goal')
    search_fields = ('full_name',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_price', 'created_at')
    search_fields = ('user__username', 'full_name')
    list_filter = ('created_at',)