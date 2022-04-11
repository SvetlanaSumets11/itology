from django.contrib.auth import views as auth_views
from django.urls import include, path

from itology.forms.login import LoginForm
from itology.views.advert_board import AdvertCreateView, AdvertDeleteView, AdvertUpdateView, AdvertView, HomeView
from itology.views.login import (
    ChangePasswordView,
    CustomLoginView,
    CustomLogoutView,
    Landing,
    RegisterView,
    ResetPasswordView,
)
from itology.views.profile import download_certificate, profile

urlpatterns = [
    path('', Landing.as_view(), name='landing'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),

    path('accounts/', include('social_django.urls', namespace='social')),
    path('logout/', CustomLogoutView.as_view(template_name='home/landing.html'), name='logout'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='login/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='login/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    path('home/', HomeView.as_view(), name='users-home'),
    path('advert/<int:pk>/', AdvertView.as_view(), name='advert'),
    path('advert/create/', AdvertCreateView.as_view(), name='advert_create'),
    path('advert/<int:pk>/update/', AdvertUpdateView.as_view(), name='advert_update'),
    path('advert/<int:pk>/delete/', AdvertDeleteView.as_view(), name='advert_delete'),

    path('certificate/<str:uuid>', download_certificate, name='download_certificate')
]
