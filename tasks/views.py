"""
🧩 tasks / views.py
Vistas de la API. Acá está toda la lógica de negocio:
CRUD de tareas con ViewSet y registro de usuarios.
"""

from rest_framework import status                         # 📋 Códigos HTTP (201, 400, 404...)
from rest_framework.response import Response              # 📤 Respuesta HTTP estandarizada de DRF
from rest_framework.views import APIView                  # 🧱 Vista base tradicional (ya no se usa, está comentada)
from .models import Task                                  # 📦 Modelo Task (models.py)
from .serializers import TaskSerializer, RegisterSerializer  # 🔄 Serializers (serializers.py)
from django.shortcuts import get_object_or_404            # 🎯 Helper: busca o devuelve 404
from rest_framework.pagination import PageNumberPagination  # 📄 Paginador
from django.conf import settings                          # ⚙️ Settings del proyecto
from rest_framework import viewsets, permissions, status  # 🧱 ViewSets + permisos
from rest_framework.decorators import action, api_view, permission_classes  # 🏷️ Decoradores DRF
from .permissions import isOwner                          # 🔒 Permiso personalizado (permissions.py)

# Create your views here.


# ═══════════════════════════════════════════════════════
# 📝 VERSIÓN MANUAL (comentada) — CRUD con APIView
# ═══════════════════════════════════════════════════════
# 
# Abajo está todo refactorizado con ViewSet, pero por si
# querés ver cómo se haría "a mano", acá están las clases:
#
# class TaskListCreateAPIView(APIView):
#     # GET  /api/tasks/   → lista paginada (con filtro opcional ?completed=true/false)
#     # POST /api/tasks/   → crear nueva tarea
#     
#     def get(self, request):
#         queryset = Task.objects.all().order_by('-created_at')
#         completed = request.query_params.get('completed')
#         if completed in ('true', 'false'):  # ── Filtro por estado ──
#             queryset = queryset.filter(completed=(completed == 'true'))
#
#         paginator = PageNumberPagination()
#         paginator.page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
#         page = paginator.paginate_queryset(queryset, request)
#
#         serializer = TaskSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
#
#     def post(self, request):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # ✅ Guardamos la tarea
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class TaskRetrieveUpdateDeleteAPIView(APIView):
#     # GET    /api/tasks/<id>/  → ver tarea individual
#     # PUT    /api/tasks/<id>/  → actualizar tarea completa
#     # PATCH  /api/tasks/<id>/  → actualizar parcial
#     # DELETE /api/tasks/<id>/  → borrar tarea
#     
#     def get_object(self, pk):
#         return get_object_or_404(Task, pk=pk)
#     
#     def get(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     
#     def delete(self, request, pk):
#         task = self.get_object(pk)
#         task.delete()  # 🗑️ Borramos la tarea
#         return Response(status=status.HTTP_204_NO_CONTENT)
# ═══════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════
# 🚀 VERSIÓN VIEWSET — mucho menos código
# ═══════════════════════════════════════════════════════
class TaskViewSet(viewsets.ModelViewSet):
    """
    🧩 TaskViewSet — CRUD completo de tareas con 2 líneas de código.
    Hereda de ModelViewSet → ya trae list, create, retrieve, update, partial_update, destroy.
    
    Registrado en tasks/urls.py con un DefaultRouter.
    Cada usuario ve SOLO sus propias tareas (owner = request.user).
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner]  # 🔒 Solo usuarios logueados + dueño de la tarea

    def get_queryset(self):
        # 📋 Filtramos: cada usuario ve únicamente sus propias tareas
        return Task.objects.filter(owner=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        # 🆕 Al crear, asignamos automáticamente el owner = usuario autenticado
        serializer.save(owner=self.request.user)
    
    def get_object(self):
        # 🔍 Buscamos una tarea dentro del queryset del usuario (solo dueño puede verla)
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
        return obj
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        ✅ Endpoint personalizado: /api/tasks/completed/
        Devuelve SOLO las tareas completadas del usuario autenticado.
        """
        # ── Filtramos tareas completadas ──
        queryset = self.get_queryset().filter(completed=True)
        # ── Paginamos ──
        page = self.paginate_queryset(queryset)
        serializer = TaskSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

# ═══════════════════════════════════════════════════════
# 📝 REGISTRO DE USUARIO
# ═══════════════════════════════════════════════════════
@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # 🚪 Cualquiera puede registrarse (sin token)
def register(request):
    """
    🆕 Registro de nuevo usuario.
    Endpoint: POST /api/auth/register/
    Recibe: { username, email, password }
    Devuelve: { id, username }
    """
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        # ✅ Datos válidos → creamos el usuario
        user = serializer.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
    
    # ❌ Datos inválidos → devolvemos errores
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
