"""
🧩 tasks / models.py
Modelo principal de la app: Task.
Cada tarea tiene título, descripción, estado, fecha y un dueño (usuario).
"""

from django.conf import settings  # ⚙️ Para referenciar el modelo de Usuario (AUTH_USER_MODEL)
from django.db import models      # 🗄️ Herramientas de BD de Django

# Create your models here.

class Task(models.Model):
    """
    📋 Modelo Task — representa una tarea del TODO.
    Cada tarea pertenece a UN usuario (owner), y un usuario puede tener muchas tareas.
    """
    title = models.CharField(max_length=200)    # 🏷️ Título de la tarea
    description = models.TextField(blank=True, null=True)  # 📝 Descripción (opcional)
    completed = models.BooleanField(default=False)          # ✅ ¿Está completada?
    created_at = models.DateTimeField(auto_now_add=True)    # 🕐 Fecha de creación (automática)
    owner = models.ForeignKey(                              # 👤 Usuario dueño de la tarea
        settings.AUTH_USER_MODEL,       # Apunta al modelo User definido en settings.py
        on_delete=models.CASCADE,       # Si el usuario se borra → se borran sus tareas
        related_name='tasks'            # 🔗 Permite hacer user.tasks para obtener sus tareas
    )

    def __str__(self):
        # 🖊️ Representación en texto: mostramos el título (útil en admin / shell)
        return self.title
