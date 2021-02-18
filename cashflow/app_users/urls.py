from django.urls import path

from app_users.views import MainPageView, UserRegisterView, UserLoginView, UserLogoutView, UserProfileView, MoneySendView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_url'),
    path('register/', UserRegisterView.as_view(), name='user_register_url'),
    path('login/', UserLoginView.as_view(), name='user_login_url'),
    path('logout/', UserLogoutView.as_view(), name='user_logout_url'),
    path('profile/', UserProfileView.as_view(), name='user_profile_url'),
    path('send/', MoneySendView.as_view(), name='send_money_url'),
]