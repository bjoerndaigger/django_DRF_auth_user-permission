from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_staff = bool(request.user and request.user.is_staff)
        return is_staff or request.method in SAFE_METHODS


class IsAdminForDeleteOrPatchAndReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # lesen funktioniert für jeden
        if request.method in SAFE_METHODS:
            return True
        # löschen nur für den Admin möglich
        elif request.method == "DELETE":
            return bool(request.user and request.user.is_superuser)
        # editieren für alle mit Staff Status möglich
        else:
            return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # lesen funktioniert für jeden
        if request.method in SAFE_METHODS:
            return True
        # löschen nur für den Admin möglich
        elif request.method == "DELETE":
            return bool(request.user and request.user.is_superuser)
        # editieren für den eingeloggten User möglich
        else:
            return bool(request.user and request.user == obj.user)



