from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics, status,permissions
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from userapi import settings
from .models import User
from .serializers import SignInSerializer,UserListCreateSerializer,UserDetailViewSerializer

# Create your views here.


class SigninView(generics.GenericAPIView):
    permission_classes = []
    serializer_class   = SignInSerializer
    authentication_classes = []
    
    def post(self,request):
        serializer = self.serializer_class(
            data=request.data, context={"request":self.request})
        if serializer.is_valid():
            return Response(serializer.validated_data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListCreateSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if 'id' in self.kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if 'id' in self.kwargs:
            queryset = self.queryset
        else:
            queryset = User.objects.filter(~Q(email=self.request.user) & ~Q(is_owner=True) & ~Q(is_superuser=True)).order_by('-id')
        return queryset

    def get_serializer_class(self):
        if 'id' in self.kwargs:
            return UserDetailViewSerializer
        else:
            return self.serializer_class

    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    