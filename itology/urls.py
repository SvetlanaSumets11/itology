from django.contrib.auth import views as auth_views
from django.urls import include, path

from itology.forms.login import LoginForm
from itology.views.advert_board import HomeView, PostCreateView, PostDeleteView, PostUpdateView, PostView
from itology.views.login import ChangePasswordView, CustomLoginView, ResetPasswordView
from itology.views.login import Landing, profile, RegisterView

urlpatterns = [
    path('', Landing.as_view(), name='landing'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),

    path('accounts/', include('social_django.urls', namespace='social')),
    path('logout/', auth_views.LogoutView.as_view(template_name='login/logout.html'), name='logout'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='login/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='login/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    path('home/', HomeView.as_view(), name='users-home'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
