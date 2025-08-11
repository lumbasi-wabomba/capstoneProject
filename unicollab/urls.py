from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewSet, TaskViewSet, MessageViewSet, NotificationViewSet, ScheduleViewSet, ResourceViewSet, UserProfileDetailView

routers = routers.DefaultRouter()
routers.register(r'projects', ProjectViewSet, basename='project')
routers.register(r'tasks', TaskViewSet, basename='task')
routers.register(r'messages', MessageViewSet, basename='message')
routers.register(r'notifications', NotificationViewSet, basename='notification')
routers.register(r'schedules', ScheduleViewSet, basename='schedule')
routers.register(r'resources', ResourceViewSet, basename='resource')

urlpatterns = [
    path('user/profile/', UserProfileDetailView.as_view(), name='user-profile'),
    path('', include(routers.urls)),   
]