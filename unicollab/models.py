from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass

class Project(models.Model):
    title = models.CharField(max_length= 200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects', db_index=True)
    members = models.ManyToManyField(User, related_name='project_members')
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"Project {self.title} created_by {self.created_by.username}"
    
class Task(models.Model):
    title = models.CharField(max_length= 200)
    description = models.TextField()
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    STATUS_CHOICES =[
        ('to_do', 'To_do'),
        ('in_progress', 'In_progress'),
        ('done', 'Done')
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, related_name='assigned_tasks') 
    due_date = models.DateField(db_index=True)
    is_public = models.BooleanField(default=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_tasks', db_index=True )

    def __str__(self):
        return f" Task {self.title} created under Project {self.project_id.title} "
    
class Resource(models.Model):
    file_url = models.URLField(editable=False, max_length=500)
    title  = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    is_public = models.BooleanField(default=True, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_resources', db_index=True)

    def __str__(self):
        return f" Resource: {self.title} has been uploaded by {self.uploaded_by.username} on {self.timestamp}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent', db_index=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_messages', db_index=True)

    def __str__(self):
        return f"message by {self.sender.username}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications', db_index=True)
    content = models.TextField()
    NOTIFICATION_TYPE_CHOICES = [
        ('reminder', 'Reminder'),
        ('update', 'Update'),
        ('mention', 'Mention'),
        ('message', 'Message')
    ]
    type = models.CharField(max_length=200, choices=NOTIFICATION_TYPE_CHOICES, db_index=True)
    is_read = models.BooleanField(default=True)

    def __str__(self):
        return f"notification for {self.user.username}"
    
class Schedule(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(blank=False, db_index=True)
    end_time = models.DateTimeField(blank=False)
    scheduled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_schedules', db_index=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_schedules')
    is_team_event = models.BooleanField(default=True)

    def __str__(self):
        return f"scheduled {self.title} under project {self.project.title} starting {self.start_time}"
    
