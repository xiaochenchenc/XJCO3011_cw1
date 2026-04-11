from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
            "admin": "/admin/",
        }
    })


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
