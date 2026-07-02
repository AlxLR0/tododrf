"""
🧩 tasks / permissions.py
Permisos personalizados para la API de tareas.
Se usan en TaskViewSet (views.py) para controlar quién puede modificar cada tarea.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS

class isOwner(BasePermission):
    """
    🔒 Solo permite acceder/modificar una tarea si el usuario autenticado es el dueño.
    Se aplica a nivel de objeto (no a nivel de lista).
    DRF lo chequea automáticamente en retrieve/update/partial_update/destroy.
    """
    def has_object_permission(self, request, view, obj):
        # ── Chequeamos que el owner_id de la tarea coincida con el user ID ──
        return getattr(obj, 'owner_id', None) == request.user.id

