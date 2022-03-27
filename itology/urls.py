from django.urls import path

from itology.views.login import home, landing, profile, RegisterView

urlpatterns = [
    path('', landing, name='landing'),
    path('home/', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]
