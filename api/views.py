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