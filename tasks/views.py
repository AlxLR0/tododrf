from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
# Create your views here.

class TaskListCreateAPIView(APIView):
    
    def get(self, request):
        queryset = Task.objects.all().order_by('-created_at')
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskRetrieveUpdateDeleteAPIView(APIView):
    
    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)
    
    def get(self, request, pk):
        #task = self.get_object(pk)
        query_set = Task.objects.all().order_by('-created_at')
        completed = request.query_params.get('completed')
        if completed in ('true', 'false'):
            query_set = query_set.filter(completed=(completed == 'true'))
        serializer = TaskSerializer(query_set, many=True)
        return Response(serializer.data)

    def put(self, request,pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)