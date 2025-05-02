from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


def user_directory_path(instance, filename):
    """Файлы загружаются в MEDIA_ROOT/users/user_<id>/<filename>"""
    return f'users/user_{instance.pk}/{filename}' if instance.pk else f'users/default/{filename}'

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        verbose_name="Фотография профиля",
        help_text="Загрузите изображение профиля"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        verbose_name="О себе",
        help_text="Напишите немного о себе",
        default=''
    )

    # Связи с группами и разрешениями (чтобы избежать конфликтов с AbstractUser)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

class Catalog(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    about_product = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='catalog/')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title



class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Catalog', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_subtotal(self):
        return self.product.price * self.quantity



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20, default='0000 0000 0000 0000')
    expiration_date = models.CharField(max_length=5, blank=True)
    cvv = models.CharField(max_length=4, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

class CalorieCalculatorResponse(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    ACTIVITY_LEVELS = [
        ('sedentary', 'Минимальная активность'),
        ('light', 'Легкая активность'),
        ('moderate', 'Умеренная активность'),
        ('active', 'Высокая активность'),
        ('very_active', 'Очень высокая активность'),
    ]

    GOALS = [
        ('lose', 'Похудение'),
        ('maintain', 'Поддержание веса'),
        ('gain', 'Набор массы'),
    ]

    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Рост в см")
    weight = models.FloatField(help_text="Вес в кг")
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS)
    goal = models.CharField(max_length=10, choices=GOALS)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.age})"
