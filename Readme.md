# Django Project Setup Guide

## Prerequisites
Ensure you have the following installed on your system before proceeding:

1. Python (3.8 or later)
2. pip (Python package manager)
3. Virtualenv (optional but recommended)
4. PostgreSQL or any other database you're using (if applicable)
5. Git
6. Node.js and npm (if your project uses a frontend build tool like webpack)

---

## Instructions to Set Up the Project

### 1. Clone the Repository

Clone the project repository from GitHub:
```bash
git clone <repository-url>
cd <project-directory>
```

---

### 2. Set Up a Virtual Environment (Optional)

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

---

### 3. Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

---

### 4. Database Migrations

Apply the database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Populate Initial Data

Run the following commands to populate initial data for categories, skill listings, and users:
```bash
python manage.py populate_categories
python manage.py populate_skill_listings
python manage.py create_users
```

---

### 6. Create a Superuser

Create an admin superuser for the project:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up a username, email, and password.

---

### 7. Collect Static Files

Collect all static files to the `staticfiles` directory:
```bash
python manage.py collectstatic
```

---

### 8. Run the Development Server

Start the Django development server:
```bash
python manage.py runserver
```
The application should now be running at `http://127.0.0.1:8000/`.

---

## Deployment

For production, you need to:
1. Set `DEBUG=False` in your `.env` file.
2. Configure your web server (e.g., Nginx or Apache).
3. Use a production-ready database (e.g., PostgreSQL).
4. Set up a WSGI/ASGI server (e.g., Gunicorn or Daphne).

Refer to the Django deployment guide for further instructions.

---

## Troubleshooting

- **Database errors**: Ensure your database is running and credentials are correct.
- **Static files not loading**: Double-check the `STATIC_ROOT` setting and run `collectstatic` again.
- **Environment variable issues**: Verify the `.env` file is correctly configured.

For further assistance, refer to the official Django documentation: https://docs.djangoproject.com/

