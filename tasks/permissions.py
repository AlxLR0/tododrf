from rest_framework.permissions import BasePermission, SAFE_METHODS

class isOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'owner_id', None) == request.user.id

