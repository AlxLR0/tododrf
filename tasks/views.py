from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from .permissions import isOwner

# Create your views here.

#forma manual de crear las crud
# class TaskListCreateAPIView(APIView):
    
#     def get(self, request):
#         queryset = Task.objects.all().order_by('-created_at')
#         completed = request.query_params.get('completed')
#         if completed in ('true', 'false'):
#             queryset = queryset.filter(completed=(completed == 'true'))

#         paginator = PageNumberPagination()
#         paginator.page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
#         page = paginator.paginate_queryset(queryset, request)

#         serializer = TaskSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TaskRetrieveUpdateDeleteAPIView(APIView):
    
#     def get_object(self, pk):
#         return get_object_or_404(Task, pk=pk)
    
#     def get(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)

#     def put(self, request,pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#forma mas facil
class TaskViewSet(viewsets.ModelViewSet):
    # queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
        return obj
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        queryset = self.get_queryset().filter(completed=True)
        page = self.paginate_queryset(queryset)
        serializer = TaskSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
