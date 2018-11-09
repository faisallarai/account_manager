from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import Http404

from api.models import Patient,MUser
from api.serializers import PatientSerializer,UserSerializer
from api.mixins import PatientMixin, UserMixin

class UserViewSet(UserMixin,viewsets.ModelViewSet):
    pass
    
    
class PatientViewSet(PatientMixin,viewsets.ModelViewSet):
   pass


class ElasticViewSet(viewsets.ViewSet):
    def list(self, request):
        item_list = get_items(request)
        return Response(data=item_list)


class AuthApi(viewsets.Rea)