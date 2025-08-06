from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserSoloDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

class UserDetail(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user  
        response = {
            'status': 'Request was permitted',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                
            }
        }
        return Response(response)
    
    
    # def post(self, request):
    #     data = request.data 
    #     return Response({'status': 'POST request permitted', 'data_received': data})

    # def patch(self, request):
    #     data = request.data  
    #     return Response({'status': 'PATCH request permitted', 'data_received': data})