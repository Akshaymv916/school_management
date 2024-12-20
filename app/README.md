# School Management System

## Description
The School Management System is a web application developed using Django that allows users to manage student details, library history, and fees history efficiently. The system implements Role-Based Access Control (RBAC) to ensure that users can access features based on their roles: Admin, Office Staff, and Librarian.

## Features
### Admin
- Full access to the system.
- Create, edit, and delete accounts for Office Staff and Librarians.
- Manage student details.
- Manage library history and fees history.

### Office Staff
- Access all student details.
- Manage (add, edit, delete) fees history.
- Review library records.
- Cannot create or delete librarian or staff accounts.

### Librarian
- View-only access to library history and student details.
- Manage borrowing records of students.
- Cannot modify student data or fees records.

## Prerequisites
- Python 3.8+
- Django 4+
- PostgreSQL or SQLite (default)

## Installation
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/school-management-system.git
    cd school-management-system
    ```

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # For Linux/Mac
    venv\Scripts\activate     # For Windows
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a Superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    Access the application at `http://127.0.0.1:8000/`

## Usage
1. **Admin Login:** Use the superuser credentials to log in as an Admin.
2. **Role Management:** Admin can create Office Staff and Librarian accounts via the Admin panel.
3. **Office Staff & Librarian Access:** Office Staff and Librarian can log in with their credentials to access their specific functionalities.

## Models
### User Roles
- **Admin** (inherits from Django's `AbstractUser`): Full control over the system.
- **Office Staff**: Restricted to fees and library management.
- **Librarian**: Limited to viewing and managing library history.

### Student Model
- `id` (Primary Key)
- `name`
- `class`
- `roll_no`
- `dob`
- `email`
- `phone`

### LibraryHistory Model
- `student` (ForeignKey to `Student`)
- `book_title`
- `borrow_date`
- `return_date`
- `status` (e.g., Borrowed/Returned)

### FeesHistory Model
- `student` (ForeignKey to `Student`)
- `fees_month`
- `amount`
- `payment_date`
- `status` (e.g., Paid/Unpaid)

## Role-Based Access Control (RBAC)
RBAC is implemented using Django's `groups` and `permissions`. Each role has predefined permissions:
- **Admin**: Access to all permissions.
- **Office Staff**: Permissions limited to student details, library reviews, and fees management.
- **Librarian**: View-only permissions for student details and library history.

## Directory Structure
```
school-management-system/
    |-- school_management/       # Main Django app
    |-- templates/               # HTML templates
    |-- static/                  # CSS, JavaScript, and images
    |-- requirements.txt         # Python dependencies
    |-- manage.py                # Django project entry point
```

## API Endpoints (Optional)
If you are exposing RESTful APIs for the system, you can implement the following endpoints:

### Students
- `GET /students/` - List all students.
- `POST /students/` - Add a new student.
- `PUT /students/<id>/` - Update student details.
- `DELETE /students/<id>/` - Delete a student.

### Library History
- `GET /library/` - List all borrowing records.
- `POST /library/` - Add a new record.
- `PUT /library/<id>/` - Update a record.

### Fees History
- `GET /fees/` - List all fees records.
- `POST /fees/` - Add a new fees record.
- `PUT /fees/<id>/` - Update a record.
- `DELETE /fees/<id>/` - Delete a record.

## Testing
Run the tests using:
```bash
python manage.py test
```

## Future Enhancements
- Add notifications for overdue library books.
- Include analytics for fees collection and borrowing patterns.
- Mobile-friendly responsive design.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
