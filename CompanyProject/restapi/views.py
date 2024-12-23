from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from .models import Client,Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializer import (ClientGetSerializer, clientPostSerializer, 
                         SingleClientSerielizer, clientUpdateSerializer, 
                         ProjectSerializer, ProjectGetSerializer, 
                         ProjectPostSerializer, 
                         UserSerializer)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
# Create your views here.


class ClientGetRetrive(APIView):
    def get(self, request,pk=None):
        if pk:
            try:
                client = Client.objects.get(pk=pk)
            except Client.DoesNotExist:
                return Response({"error":"Client not found"},status=status.HTTP_404_NOT_FOUND)
            
            serializer = SingleClientSerielizer(client)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
        client = Client.objects.all()
        serializer = ClientGetSerializer(client,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    
    def post(self,request):
        serializer_class = clientPostSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data,status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request,pk):
        try:
            client = Client.objects.get(pk=pk)
        except:
            return Response({"error":"Data is not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = clientUpdateSerializer(client,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
    # def put(self,request,pk):
    #     try:
    #         client = Client.objects.get(pk=pk)
    #     except Client.DoesNotExist:
    #         return Response({"error":"Data is not found"},status=status.HTTP_404_NOT_FOUND)
        
    #     serializer = clientPostSerializer(client, data=request.data, partial=False)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    
    
    
# class ClientCreate(APIView):
    
@api_view(["PUT"])
def put_client_data(request,pk):
    if request.method == 'PUT':
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({"error":"Data is not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = clientUpdateSerializer(client, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
@api_view(["DELETE"])
def delete_data(reqeuest,pk):
    if reqeuest.method == "DELETE":
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({"error":"Data is not found"},status=status.HTTP_404_NOT_FOUND)
        
        if(client):
            client.delete()
            return Response({"Successfull":f"Data is deleted {client}"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"Some thing went wrong"},status=status.HTTP_400_BAD_REQUEST)
    


    
class ProjectGetRetrive(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                project = Project.objects.get(pk=pk)
            except Project.DoesNotExist:
                return Response({"error":"Data is not found"},status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)

        project = Project.objects.all()
        serializer = ProjectGetSerializer(project,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # project = project.objects.all()
        serializer = ProjectPostSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            projectResSerializer = ProjectSerializer(project)

            return Response(projectResSerializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, rqeuest, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error":"Data is not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializers = ProjectPostSerializer(project)
        return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
    



@api_view(["DELETE"])
def delete_project(request,pk):
    if request.method == "DELETE":
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error: Data is not found"},status=status.HTTP_404_NOT_FOUND)
        
        if project:
            project.delete()
            return Response({"Successfull":f"Data is deleted {project}"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"Some thing wen wrong"},status=status.HTTP_400_BAD_REQUEST)
    

class ResgisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
    # if request.method == 'POST':
      username = request.data.get('username')
      email = request.data.get('email')
      password = request.data.get('password')
      if User.objects.filter(username=username).exists():
          return Response({"error":"Username already exist"},status=status.HTTP_400_BAD_REQUEST)
      
      if User.objects.filter(email=email).exists():
          return Response({"error":"Email already exists"},status=status.HTTP_400_BAD_REQUEST)
      
      user = User.objects.create(username=username, email=email, password=make_password(password))
      user.save()
      return Response({"messgae":"User created successfully"}, status=status.HTTP_201_CREATED)
    




class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token":token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error":"Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def user_view(request,pk=None):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error":"data is not found"}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.all()
        serializer = UserSerializer(User)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserView(APIView):
    def get(self,request, pk=None):
        if pk:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({"error":"data is not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        user = User.objects.all()
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    






