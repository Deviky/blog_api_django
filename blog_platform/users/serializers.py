from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Поле пароля только для записи

    class Meta:
        model = get_user_model()  # Используем кастомную модель пользователя
        fields = ('id', 'username', 'email', 'bio', 'password')  # Добавили поле пароля

    def create(self, validated_data):
        # Создаём пользователя, хешируя пароль
        password = validated_data.pop('password')  # Убираем пароль из данных
        user = super().create(validated_data)
        user.set_password(password)  # Хешируем пароль
        user.save()  # Сохраняем пользователя
        return user

class UserDetailWithPostsSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()  # ✅ Явно добавляем поле

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'posts')

    def get_posts(self, obj):
        from blog.serializers import PostSerializer  # импорт внутри метода — ОК
        posts = obj.post_set.all()  # ⚠️ Используем default related_name
        return PostSerializer(posts, many=True).data