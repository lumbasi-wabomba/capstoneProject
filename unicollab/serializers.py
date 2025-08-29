from rest_framework import serializers
from .models import User, Project, Task, Resource, Message, Notification, Schedule
from datetime import date, datetime

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        read_only_fields = ['created_by', 'members']
        fields = ['title', 'description', 'is_public', 'created_by', 'members']

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field='title', queryset=Project.objects.all())
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    due_date = serializers.DateField()

    class Meta:
        model = Task
        read_only_fields = ['assigned_to', 'project']
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'is_public', 'assigned_to', 'project']


    def validate(self, attrs):
        due_date = attrs.get("due_date")
        if due_date and due_date < date.today():
            raise serializers.ValidationError({"due_date": "Due date cannot be in the past."})
        return attrs

class ResourceSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(read_only=True)
    project = serializers.SlugRelatedField(slug_field='title', queryset=Project.objects.all())
    uploaded_by = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
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
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    project = serializers.SlugRelatedField(slug_field='title', queryset=Project.objects.all())
    scheduled_by = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all()) 
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['scheduled_by', 'project']

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        
        if start_time > end_time and end_time < datetime.now():
            raise serializers.ValidationError("there's an error with your time plan. End time is incorrect")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many=True, read_only=True, source='created_projects')
    tasks = TaskSerializer(many=True, read_only=True, source='assigned_tasks')
    notifications = NotificationSerializer(many=True, read_only=True, source='user_notifications')
    schedule = ScheduleSerializer(many=True, read_only=True, source='user_schedules')
    resources = ResourceSerializer(many=True, read_only=True, source='uploaded_files')

    class Meta:
        model = User
        fields = ['project', 'tasks', 'notifications', 'schedule', 'id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'resources']
        read_only_fields =['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user