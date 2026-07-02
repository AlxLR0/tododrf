"""
🧩 tasks / urls.py
Rutas de la API de tareas.
Usamos un DefaultRouter de DRF para generar automáticamente
las rutas CRUD del TaskViewSet.
"""

# ── Versión anterior (manual con APIView) ──────────────────
# from django.urls import path
# from .views import TaskListCreateAPIView, TaskRetrieveUpdateDeleteAPIView
#
# urlpatterns = [
#     path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
#     path('tasks/<int:pk>/', TaskRetrieveUpdateDeleteAPIView.as_view(), name='task-retrieve-update-delete'),
# ]
# ──────────────────────────────────────────────────────────

# 🔌 Router de DRF — genera automáticamente:
#   GET    /api/tasks/          → listar tareas
#   POST   /api/tasks/          → crear tarea
#   GET    /api/tasks/{id}/     → ver tarea
#   PUT    /api/tasks/{id}/     → actualizar tarea
#   PATCH  /api/tasks/{id}/     → actualizar parcial
#   DELETE /api/tasks/{id}/     → borrar tarea
#   GET    /api/tasks/completed/ → endpoint personalizado ✅
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')  # 📍 Registramos el ViewSet

# Las rutas generadas se incluyen desde tododrf/urls.py bajo /api/
urlpatterns = router.urls