
## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Contributing](#contributing)
---
## Features
- **Employee Management**:
  - Add, update, and delete employee details.
  - Upload profile photos and documents (e.g., appointment letters, offer letters).
  - Assign departments, positions, and reporting managers.
- **Role-Based Access**:
  - Automatically create user accounts with roles (e.g., "Employee").
  - Restrict access based on user roles.
- **Asset Management**:
  - Track assets assigned to employees.
  - Retain asset records even after employee deletion.
- **Exit Management**:
  - Manage exit details, including clearance forms and relieving letters.
- **Search and Filter**:
  - Search employees by name, ID, department, designation, or date of joining.
- **Validation**:
  - Validate file uploads (e.g., size limits, allowed file types).
---
## Prerequisites
Before setting up the project, ensure you have the following installed:
- Python 3.8 or higher
- Django 4.x
- PostgreSQL or MySQL (for database)
- Node.js and npm (if using frontend tools like Toastr.js)
---
## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nitinadhikari01/HRMS.git
   cd HRMS
   ```
2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   
3. **Set Up the Database**:
   - Update the database settings in `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'your_db_name',
             'USER': 'your_db_user',
             'PASSWORD': 'your_db_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```
   - Run migrations:
     ```bash
     python manage.py migrate
     ```
4. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
6. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.
---
## Project Structure
```
hrms/
├── manage.py                  # Django management script
├── README.md                  # Project documentation
├── Department_Designation/    # Department and Designation application directory
├── employee_app/              # Employee/user application directory
├── employee_information/      # Hr/Admin application directory
│   ├── migrations/            # Database migrations
│   ├── templates/             # HTML templates
│   ├── admin.py               # Admin configurations
│   ├── apps.py                # App configurations
│   ├── models.py              # Database models
│   ├── urls.py                # URL routing
│   ├── views.py               # View logic
├── media/                     # Uploaded files (e.g., profile photos, documents)
├── static/                    # Static files (CSS, JS, images) 
└── ...
```
---
## Usage
### Adding an Employee
1. Navigate to the "Add Employee" page.
2. Fill in the required fields (e.g., name, email, department).
3. Upload a profile photo and relevant documents.
4. Save the form to create the employee.
### Managing Assets
1. Assign assets to employees via the "Assets" section.
2. View or update asset details as needed.
### Deleting an Employee
1. Delete an employee from the admin panel or UI.
2. Assets will retain their records but will be unassigned (`employee = NULL`).
---
## API Endpoints
| Endpoint                     | Method | Description                          |
|------------------------------|--------|--------------------------------------|
| `/api/employees/`            | GET    | Retrieve a list of all employees.    |
| `/api/employees/<id>/`       | GET    | Retrieve details of a specific employee. |
| `/api/employees/create/`     | POST   | Create a new employee.               |
| `/api/employees/update/<id>/`| PUT    | Update an existing employee.         |
| `/api/employees/delete/<id>/`| DELETE | Delete an employee.                  |
---
## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your descriptive message"
   ```
4. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request describing your changes.
---
## License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
---
