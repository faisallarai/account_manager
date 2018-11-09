from rest_framework import generics, permissions

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from api.serializers import PatientSerializer, UserSerializer
from api.models import Patient, MUser

class PatientMixin(object):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Patient.objects.active()
    serializer_class = PatientSerializer
    

class UserMixin(object):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = MUser.objects.active()
    serializer_class = UserSerializer


