from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Employee


class EmployeeAPITestCase(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            emp_id=1001,
            first_name='Alice',
            last_name='Zhang',
            email='alice.zhang@example.com',
            department='Engineering',
            position='Software Engineer',
            hire_date='2024-08-01',
            salary='58000.00',
        )

    def test_list_employees(self):
        url = reverse('employee-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_employee(self):
        url = reverse('employee-list')
        payload = {
            'emp_id': 1002,
            'first_name': 'Bob',
            'last_name': 'Smith',
            'email': 'bob.smith@example.com',
            'department': 'Sales',
            'position': 'Account Manager',
            'hire_date': '2025-01-15',
            'salary': '45000.00',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.filter(emp_id=1002).count(), 1)

    def test_search_employees(self):
        url = reverse('employee-search')
        response = self.client.get(url, {'query': 'Alice'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
