from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,filters
from restapi import serializers
from restapi import models

from rest_framework.authentication import TokenAuthentication
from restapi import permissions

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework.permissions import IsAuthenticatedOrReadOnly

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self,request,format=None):
        """returns a list of api view features"""

        an_apiview = [
            'Uses HTTP methods as function (get,post,patch,put,delete)',
    
            'Is similar to a traditional django view',
            'Gives you most control over application logic',
            'is mapped manually to urls',
        ]
        return Response({'message':'hello','an_apiview': an_apiview})


    def post(self,request):
        """create a hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                    )


    def put(self,request,pk=None):
        """handle updating an object"""
        return Response({'method':'PUT'})

    def patch(self,request,pk=None):
        """handle a partial update of an object"""
        return Response({'method':'PATCH'})

    def delete(self,request,pk=None):
        """delete an object"""
        return Response({'method':'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloSerializer
    """test api viewset"""
    def list(self,request):
        """Return a hello message"""
        a_viewset=[
            'Uses actions (list,create,retrive,update,partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello', 'a_viewset':a_viewset})

    def create(self,request):
        """create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})

        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

    def retrive(self,request,pk=None):
        """handle geting an object by its id"""
        return Response({'http_method': 'GET'})

    def update(self,request,pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self,request,pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self,response,pk=None):
        """Handel removing an object"""
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )

    def perform_create(self,serializer):
        """sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)