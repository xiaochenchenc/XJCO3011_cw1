from django.db import models

class Employee(models.Model):
    emp_id = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    department = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=50, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['emp_id']

    def __str__(self) -> str:
        return f'{self.emp_id}: {self.first_name} {self.last_name}' 