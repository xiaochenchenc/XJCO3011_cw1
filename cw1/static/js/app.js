// Employee Management System JavaScript

const API_BASE = '/api';

// Load employees on page load
document.addEventListener('DOMContentLoaded', function() {
    loadEmployees();
    loadStats();

    // Add employee form handler
    document.getElementById('addEmployeeForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addEmployee();
    });
});

// Load all employees
async function loadEmployees() {
    try {
        const response = await fetch(`${API_BASE}/employees/`);
        const data = await response.json();
        displayEmployees(data);
    } catch (error) {
        console.error('Error loading employees:', error);
        showAlert('Error loading employees', 'danger');
    }
}

// Load department statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/employees/stats/`);
        const data = await response.json();
        displayStats(data.department_counts);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Display employees in table
function displayEmployees(employees) {
    const container = document.getElementById('employeesList');

    if (employees.length === 0) {
        container.innerHTML = '<p class="text-muted">No employees found.</p>';
        return;
    }

    let html = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Department</th>
                        <th>Position</th>
                        <th>Hire Date</th>
                        <th>Salary</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
    `;

    employees.forEach(employee => {
        const hireDate = employee.hire_date ? new Date(employee.hire_date).toLocaleDateString() : '';
        const salary = employee.salary ? `$${parseFloat(employee.salary).toLocaleString()}` : '';

        html += `
            <tr>
                <td>${employee.emp_id}</td>
                <td>${employee.first_name} ${employee.last_name}</td>
                <td>${employee.email}</td>
                <td>${employee.department || ''}</td>
                <td>${employee.position || ''}</td>
                <td>${hireDate}</td>
                <td>${salary}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editEmployee(${employee.id})">Edit</button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteEmployee(${employee.id})">Delete</button>
                </td>
            </tr>
        `;
    });

    html += `
                </tbody>
            </table>
        </div>
    `;

    container.innerHTML = html;
}

// Display department statistics
function displayStats(stats) {
    const container = document.getElementById('stats');

    if (!stats || stats.length === 0) {
        container.innerHTML = '';
        return;
    }

    let html = '<div class="row">';

    stats.forEach(stat => {
        html += `
            <div class="col-md-3 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">${stat.department || 'No Department'}</h5>
                        <h3 class="text-primary">${stat.total}</h3>
                        <p class="card-text">Employees</p>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    container.innerHTML = html;
}

// Add new employee
async function addEmployee() {
    const employeeData = {
        emp_id: parseInt(document.getElementById('empId').value),
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        department: document.getElementById('department').value,
        position: document.getElementById('position').value,
        hire_date: document.getElementById('hireDate').value || null,
        salary: document.getElementById('salary').value ? parseFloat(document.getElementById('salary').value) : null,
    };

    try {
        const response = await fetch(`${API_BASE}/employees/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(employeeData),
        });

        if (response.ok) {
            showAlert('Employee added successfully!', 'success');
            document.getElementById('addEmployeeForm').reset();
            loadEmployees();
            loadStats();
        } else {
            const error = await response.json();
            showAlert(`Error: ${JSON.stringify(error)}`, 'danger');
        }
    } catch (error) {
        console.error('Error adding employee:', error);
        showAlert('Error adding employee', 'danger');
    }
}

// Search employees
async function searchEmployees() {
    const query = document.getElementById('searchInput').value.trim();

    if (!query) {
        loadEmployees();
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/employees/search/?query=${encodeURIComponent(query)}`);
        const data = await response.json();
        displayEmployees(data);
    } catch (error) {
        console.error('Error searching employees:', error);
        showAlert('Error searching employees', 'danger');
    }
}

// Edit employee
async function editEmployee(id) {
    try {
        const response = await fetch(`${API_BASE}/employees/${id}/`);
        const employee = await response.json();

        // Populate edit form
        document.getElementById('editEmployeeId').value = employee.id;
        document.getElementById('editEmpId').value = employee.emp_id;
        document.getElementById('editFirstName').value = employee.first_name;
        document.getElementById('editLastName').value = employee.last_name;
        document.getElementById('editEmail').value = employee.email;
        document.getElementById('editDepartment').value = employee.department || '';
        document.getElementById('editPosition').value = employee.position || '';
        document.getElementById('editHireDate').value = employee.hire_date || '';
        document.getElementById('editSalary').value = employee.salary || '';

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('editModal'));
        modal.show();
    } catch (error) {
        console.error('Error loading employee:', error);
        showAlert('Error loading employee details', 'danger');
    }
}

// Update employee
async function updateEmployee() {
    const id = document.getElementById('editEmployeeId').value;
    const employeeData = {
        emp_id: parseInt(document.getElementById('editEmpId').value),
        first_name: document.getElementById('editFirstName').value,
        last_name: document.getElementById('editLastName').value,
        email: document.getElementById('editEmail').value,
        department: document.getElementById('editDepartment').value,
        position: document.getElementById('editPosition').value,
        hire_date: document.getElementById('editHireDate').value || null,
        salary: document.getElementById('editSalary').value ? parseFloat(document.getElementById('editSalary').value) : null,
    };

    try {
        const response = await fetch(`${API_BASE}/employees/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(employeeData),
        });

        if (response.ok) {
            showAlert('Employee updated successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
            loadEmployees();
            loadStats();
        } else {
            const error = await response.json();
            showAlert(`Error: ${JSON.stringify(error)}`, 'danger');
        }
    } catch (error) {
        console.error('Error updating employee:', error);
        showAlert('Error updating employee', 'danger');
    }
}

// Delete employee
async function deleteEmployee(id) {
    if (!confirm('Are you sure you want to delete this employee?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/employees/${id}/`, {
            method: 'DELETE',
        });

        if (response.ok) {
            showAlert('Employee deleted successfully!', 'success');
            loadEmployees();
            loadStats();
        } else {
            showAlert('Error deleting employee', 'danger');
        }
    } catch (error) {
        console.error('Error deleting employee:', error);
        showAlert('Error deleting employee', 'danger');
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container');
    container.insertBefore(alertContainer, container.firstChild);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}