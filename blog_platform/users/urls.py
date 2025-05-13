from django.urls import path
from .views import UserCreateView, UserDetailView, UserWithPostsView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/', UserWithPostsView.as_view(), name='user-with-posts'),
]
