from django.urls import path
from accounts import views
from .views import sign_up
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import index
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path(' ', views.index, name='home'),  # Главная страница
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('survey/', views.survey, name='survey'),
    path('basket/', views.basket, name='basket'),
    path('add-to-cart/<int:product_id>/', views.index, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('clear-cart/', views.clear_basket, name='clear_basket'),
    path("chat/", views.chat_bot, name="chat_bot"),
    path("chat-bot/", views.chat_page, name="chat_page"),
    path("gp_helper/", views.gp_helper_view, name='gp_helper'),
    path('chat_combined/', views.chat_combined, name='chat_combined'),
    path('login/', views.log_in, name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset_form'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', LogoutView.as_view(next_page='signup'), name='logout')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)