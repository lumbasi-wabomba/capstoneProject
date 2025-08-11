from rest_framework import serializers
from .models import User, Project, Task, Resource, Message, Notification, Schedule
from datetime import date, datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        read_only_fields = ['created_by', 'members']
        fields = ['title', 'description', 'is_public', 'created_by', 'members']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ['assigned_to', 'project']
        fields = ['title', 'description', 'status', 'due_date', 'is_public', 'assigned_to', 'project']

    def validate(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value 


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'timestamp','project']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Message
        fields = '__all__'
        read_only_fields = ['sender', 'timestamp', 'project']

    def validate(self, attrs):
        project = attrs['project']
        request = self.context.get('request')
        user = request.user

        if not project.members.filter(id=user.id).exists():
            raise serializers.ValidationError("you must be a member to send a message")
        return attrs



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['scheduled_by']

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        
        if start_time > end_time and end_time < datetime.now():
            raise serializers.ValidationError("there's an error with your time plan. End time is incorrect")
        return attrs
