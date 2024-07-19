from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, ContributorSerializer
from .models import Contributor


class UserViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated, )

    def list(self, request):
        user = User.objects.get(username=request.user)
        user_data = UserSerializer(user).data
        return Response(user_data)


class ContributorViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
