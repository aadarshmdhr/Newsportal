from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from api.serializers import CategorySerializer, GroupSerializer, PostSerializer, TagSerializer, UserSerializer
from newspaper.models import Category, Post, Tag


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
            if self.action in ["list", "retrieve"]:
                return [permissions.AllowAny()]
            
            return super().get_permissions()


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
         if self.action in ["list", "retrieve"]:
              return [permissions.AllowAny()]
         
         return super().get_permissions()
    

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Posts to be viewed or edited.
    """

    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
         if self.action in ["list", "retrieve"]:
              return [permissions.AllowAny()]
         
         return super().get_permissions()