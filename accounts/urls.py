from django.urls import path
from .views import RegisterView, LoginView, VerifyEmailView, ChangePasswordView, \
    UpdateProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='ragister'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-verify/', VerifyEmailView.as_view(), name="email-verify"),

    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
]
