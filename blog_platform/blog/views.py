from django.core.cache import cache
from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from django.core.cache import cache

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f'post:{pk}'
        post = cache.get(cache_key)

        if post is None:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            post = serializer.data
            cache.set(cache_key, post, timeout=60 * 5)
        return Response(post)

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # Можно не кешировать, потому что retrieve создаст кэш при первом обращении

    def perform_update(self, serializer):
        post = serializer.save()
        cache_key = f'post:{post.pk}'
        cache.delete(cache_key)

    def perform_destroy(self, instance):
        cache_key = f'post:{instance.pk}'
        instance.delete()
        cache.delete(cache_key)
