from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, api_root, index, CustomAuthToken, register_user

router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', index, name='index'),
    # Stable JSON discovery (DRF's GET /api/ is the browsable router root instead).
    path('api/info/', api_root, name='api_info'),
    path('api/', include(router.urls)),
    path('api/auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('api/auth/register/', register_user, name='api_register'),
]
