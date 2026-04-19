from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'export_id',
            'emp_id',
            'first_name',
            'last_name',
            'email',
            'department',
            'position',
            'hire_date',
            'salary',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'export_id', 'created_at', 'updated_at']
