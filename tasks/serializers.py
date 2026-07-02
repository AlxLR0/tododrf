"""
🧩 tasks / serializers.py
Serializers de la app Tasks.
Convierten objetos Python (modelos) a JSON y viceversa.
"""

from rest_framework import serializers       # 🔄 Base de DRF para serializers
from .models import Task                     # 📦 Modelo Task (models.py)
from django.contrib.auth import get_user_model  # 👤 Obtenemos el modelo User activo

User = get_user_model()  # 👤 Referencia al modelo de usuario (el que define settings.AUTH_USER_MODEL)

class TaskSerializer(serializers.ModelSerializer):
    """
    📋 Serializer para el modelo Task.
    Se usa en TaskViewSet (views.py) para todas las operaciones CRUD.
    """
    owner = serializers.ReadOnlyField(source='owner.username')  # 👤 Muestra el username en vez del ID
    
    class Meta:
        model = Task
        fields = '__all__'                               # 📦 Todos los campos del modelo
        read_only_fields = ('created_at', 'owner')       # 🔒 El owner y created_at los asigna el sistema, no el usuario

class RegisterSerializer(serializers.ModelSerializer):
    """
    🆕 Serializer para registrar nuevos usuarios.
    Se usa en la vista register() (views.py).
    Endpoint: POST /api/auth/register/
    """
    password = serializers.CharField(write_only=True, min_length=8)  # 🔑 Password mínimo 8 caracteres

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # 🚫 Nunca se devuelve en la respuesta
        }

    def create(self, validated_data):
        """
        🏗️ Crea un usuario usando create_user (hashea la password automáticamente).
        Recibe los datos ya validados del serializer.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  # 🔐 Django la hashea automáticamente
        )
        return user  # ✅ Devolvemos el usuario creado