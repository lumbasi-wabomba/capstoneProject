from django.contrib import admin
from .models import User, Project, Task, Resource, Message, Notification, Schedule
# Register your models here.

admin.register(User)
admin.register(Project)
admin.register(Task)
admin.register(Resource)
admin.register(Message)
admin.register(Notification)
admin.register(Schedule)