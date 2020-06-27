from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import RegisterView, ChangePasswordView, profile, farm_coordinates

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name="login"),
    path('signup/', RegisterView.as_view(), name="signup"),
    path('profile/', profile, name="profile"),
    path('farm-coordinates/', farm_coordinates, name="farm-coordinates"),
    path('change-pass/', ChangePasswordView.as_view(), name="change-password"),
    path('forget-pass/', auth_views.PasswordResetView.as_view(template_name="user/forget-password.html"), name="reset_password"),
    path('forget-pass/done', auth_views.PasswordResetDoneView.as_view(template_name="user/forget-password-done.html"), name="password_reset_done"),
    path('forget-pass/confirm/<str:uidb64>/<str:token>', auth_views.PasswordResetConfirmView.as_view(template_name="user/forget-password-set.html"), name="password_reset_confirm"),
    path('forget-pass/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="user/password-reset-completed.html"), name="password_reset_complete"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)