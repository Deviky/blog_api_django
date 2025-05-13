from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserSerializer, UserDetailWithPostsSerializer
from django.contrib.auth import get_user_model

class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        self.user = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        refresh = RefreshToken.for_user(self.user)
        response.data = {
            'user': response.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return response

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserWithPostsView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailWithPostsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user and not request.user.is_staff:
            return Response({'detail': 'Недостаточно прав.'}, status=403)
        return super().delete(request, *args, **kwargs)
