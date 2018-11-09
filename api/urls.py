from django.urls import include,path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'account'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'patients', views.PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
