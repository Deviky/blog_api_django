from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение: только автор может редактировать или удалять пост.
    Остальные могут только просматривать (GET).
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить безопасные методы (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить редактирование/удаление только автору
        return obj.author == request.user