# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  RegisterView, LoginView, LogoutView,UserViewSet, ProjectViewSet, TaskViewSet,ScheduleViewSet, ResourceViewSet, NotificationViewSet,MessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("", include(router.urls)),
]