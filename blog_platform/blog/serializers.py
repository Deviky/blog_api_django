from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer



class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author',)
