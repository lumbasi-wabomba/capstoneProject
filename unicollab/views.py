from django.contrib.auth import authenticate
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import User, Project, Task, Resource, Message, Notification, Schedule
from .serializers import (
    UserSerializer, ProjectSerializer, TaskSerializer,
    ResourceSerializer, MessageSerializer, NotificationSerializer,
    ScheduleSerializer
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user) | Project.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        project.members.add(self.request.user)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        project = self.get_object()
        serializer = UserSerializer(project.members.all(), many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ('status', 'priority')

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user) | Task.objects.filter(is_public=True)

    @action(methods=['post'], detail=True)
    def assign(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(pk=user_id)
            task.assigned_to.add(user)
            return Response({"success": f"{task.title} assigned to {user.username}"})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class ScheduleViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(scheduled_by=self.request.user)

class ResourceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ResourceSerializer

    def get_queryset(self):
        return Resource.objects.filter(is_public=True) | Resource.objects.filter(uploaded_by=self.request.user)

class NotificationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = NotificationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['type']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(project__members=self.request.user) | Message.objects.filter(sender=self.request.user)
