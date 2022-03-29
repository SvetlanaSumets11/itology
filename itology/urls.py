from django.urls import path

from itology.views.advert_board import HomeView, PostCreateView, PostDeleteView, PostUpdateView, PostView
from itology.views.login import home, landing, profile, RegisterView

urlpatterns = [
    path('', landing, name='landing'),
    path('home/', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),

    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
