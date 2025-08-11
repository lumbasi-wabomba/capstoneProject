from django.shortcuts import render
from .models import User, Project, Task, Resource, Message, Notification, Schedule
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, ResourceSerializer, MessageSerializer, NotificationSerializer, ScheduleSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters

# Create your views here.
class UserProfileDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_object(self):
        return self.request.user
    

class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
   
    def get_queryset(self):
        return Project.objects.filter(members= self.request.user) | Project.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        project.members.add(self.request.user)

    @action(detail=True, methods=['get'])
    def members(self):
        project = self.get_object()
        serializer = UserSerializer(project.members.all(), many=True)
        return Response(serializer.data)
    


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ('status', 'priority')


    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user) | Task.objects.filter(is_public=True)
    
    @action(methods=['post'], detail=True)
    def assign_task(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            task.assigned_to.add(user)
            return Response(f"{task.title} has been assigned to {user.username} ")
        except User.DoesNotExist:
             return Response({'error': 'User not found'}, status=404)

class ScheduleViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(scheduled_by= self.request.user)
    
class ResourceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_queryset(self):
        return Resource.objects.filter(is_public=True) | Resource.objects.filter(uploaded_by=self.request.user)
    
class NotificationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Notification.objects.all()   
    serializer_class = NotificationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['type']

class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Message.objects.all()      
    serializer_class = MessageSerializer

    def get_queryset(self):
      return Message.objects.filter(project__members=self.request.user) | Message.objects.filter(sender=self.request.user)
