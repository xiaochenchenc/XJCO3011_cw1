from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .models import Employee
from .serializers import EmployeeSerializer


def index(request):
    """Main web interface for employee management."""
    return render(request, 'index.html')


def api_root(request):
    """API root endpoint with available endpoints."""
    return JsonResponse({
        "message": "Employee Management API",
        "version": "1.0",
        "endpoints": {
            "employees": "/api/employees/",
            "search": "/api/employees/search/?query={text}",
            "stats": "/api/employees/stats/",
            "auth": "/api/auth/",
            "admin": "/admin/",
        }
    })


class CustomAuthToken(ObtainAuthToken):
    """Custom authentication token view with user info."""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """User registration endpoint."""
    from django.contrib.auth.models import User
    from django.contrib.auth.hashers import make_password

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([username, email, password]):
        return Response(
            {'error': 'Username, email, and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.pk,
        'email': user.email,
        'username': user.username,
        'message': 'User created successfully'
    }, status=status.HTTP_201_CREATED)


class EmployeeViewSet(viewsets.ModelViewSet):
    """Employee CRUD API plus analytics and search endpoints."""

    queryset = Employee.objects.all().order_by('emp_id')
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return employee counts grouped by department."""
        department_counts = (
            Employee.objects
            .values('department')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        return Response({'department_counts': list(department_counts)})

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search employees by name, department or position."""
        query = request.query_params.get('query', '').strip()
        if not query:
            return Response(
                {'detail': 'The query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.queryset.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(department__icontains=query)
            | Q(position__icontains=query)
            | Q(email__icontains=query)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
