"""
🧩 tododrf / urls.py (raíz)
Acá se conectan todas las rutas del proyecto.
Básicamente: panel admin, API de tareas, y auth (registro + JWT).
"""

from django.contrib import admin                    # 🏠 Panel admin de Django
from django.urls import path, include               # 🔗 Para armar rutas
from tasks.views import register                    # 📝 Vista de registro (vive en tasks/views.py)
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)  # 🔑 JWT tokens

urlpatterns = [
    # 🏠 Admin de Django
    path('admin/', admin.site.urls),

    # 📦 API de tareas — redirige a tasks/urls.py (router del ViewSet)
    path('api/', include('tasks.urls')),

    # 🔐 Autenticación
    path('api/auth/register/', register, name='register'),                  # 📝 Registro de usuario
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 🔑 Login (da access + refresh token)
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),        # ♻️ Refrescar token
]
