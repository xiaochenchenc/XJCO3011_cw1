from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, api_root, index

router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
]
