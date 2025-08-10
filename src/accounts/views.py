from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.pagination import CursorPagination
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    """
    View to create a user. Anyone can access this endpoint.
    """
        
    queryset = User.objects.all() # which object to create
    serializer_class = UserSerializer # which serializer to use
    permission_classes = [permissions.AllowAny] # allow anyone to access

class UserCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'id'


class UserListAPIView(generics.ListAPIView):
    """ 
    View to list all Users. Only authenticated users can view.
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = UserCursorPagination

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ 
    View to retrieve, update, or delete a User. Only authenticated users can access this.
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
