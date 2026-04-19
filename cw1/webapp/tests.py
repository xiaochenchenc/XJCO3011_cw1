import json
import tempfile
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Employee


class EmployeeAPITestCase(APITestCase):
    def setUp(self):
        # Create test user and token
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

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

    def test_api_info_json_index(self):
        response = self.client.get('/api/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('application/json', response['Content-Type'])
        self.assertIn('endpoints', response.json())

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

    def test_detail_lookup_by_emp_id_when_not_pk(self):
        other = Employee.objects.create(
            emp_id=91006,
            first_name='Pat',
            last_name='Lee',
            email='pat.lee91006@example.com',
            department='Ops',
            position='Analyst',
            hire_date='2023-02-02',
            salary='51000.00',
        )
        url = reverse('employee-detail', kwargs={'pk': other.emp_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], other.email)

    def test_search_numeric_matches_emp_id(self):
        url = reverse('employee-search')
        response = self.client.get(url, {'query': str(self.employee.emp_id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['emp_id'], self.employee.emp_id)

    def test_detail_lookup_by_json_export_id(self):
        other = Employee.objects.create(
            export_id=6,
            emp_id=91007,
            first_name='Frank',
            last_name='Wilson',
            email='frank.wilson91007@example.com',
            department='Finance',
            position='Financial Analyst',
            hire_date='2023-09-18',
            salary='51000.75',
        )
        url = reverse('employee-detail', kwargs={'pk': 6})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['emp_id'], other.emp_id)
        self.assertEqual(response.data['export_id'], 6)


class ImportEmployeesJsonCommandTests(TestCase):
    def test_import_ignores_id_and_timestamps(self):
        payload = [
            {
                "id": 4242,
                "emp_id": 777001,
                "first_name": "Json",
                "last_name": "Import",
                "email": "json.import.test@example.com",
                "department": "QA",
                "position": "Tester",
                "hire_date": "2024-01-02",
                "salary": "10000.00",
                "created_at": "2020-01-01T00:00:00Z",
                "updated_at": "2020-01-02T00:00:00Z",
            }
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump(payload, tmp)
            path = tmp.name
        try:
            call_command("import_employees_json", json_path=path)
        finally:
            Path(path).unlink(missing_ok=True)

        obj = Employee.objects.get(emp_id=777001)
        self.assertEqual(obj.export_id, 4242)
        self.assertNotEqual(obj.id, 4242)
        self.assertEqual(obj.first_name, "Json")
