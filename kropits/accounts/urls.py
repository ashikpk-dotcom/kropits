from django.urls import path
from .views import RegisterView, LoginView, SetLanguageView, register_page, login_page

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', login_page, name='refresh'),
    path('set-language/', SetLanguageView.as_view(), name='set-language'),
    path('register-page/', register_page, name='register-page'),
    path('login-page/', login_page, name='login-page'),
]
