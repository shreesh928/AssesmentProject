from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['date_joined']


# For client serializers
class ClientGetSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')  # Display username of the creator

    class Meta:
        model = Client
        fields = ["id","client_name","created_by"]


class clientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id","client_name","created_by"]
        read_only = ["created_by"]


class ClientProjectSerielizer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","project_name"]

class SingleClientSerielizer(serializers.ModelSerializer):
    projects = ClientProjectSerielizer(many=True, read_only=True)
    created_by = serializers.CharField(source="created_by.username")
    class Meta:
        model = Client
        fields = ["id","client_name","projects","created_at","created_by"]


class clientUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username")
    class Meta:
        model = Client
        fields = ["id","client_name","created_by","created_at","updated_at"]
        read_only = ["created_by","created_at","updated_at"]



# For project serializers

class UserPropjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username"]

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source="client.client_name")
    created_by = serializers.CharField(source="created_by.username")   
    users = UserPropjectSerializers(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ["id","project_name","client","users","created_at","created_by"]


class ProjectGetSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username")
    client = serializers.CharField(source="client.client_name")
    class Meta:
        model = Project
        fields = ["id","project_name","client","created_at","created_by"]


class ProjectPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["project_name","client","users","created_by"]





