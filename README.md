# Secure Student Resource Sharing Portal

A cloud-based secure web application developed as part of the DevSecOps capstone project.

## Features
- User registration and login
- Password hashing
- Role-based access control
- Student resource upload
- Secure file type validation
- Admin dashboard
- Docker containerization
- Security headers

## Technologies Used
- Python Flask
- SQLite
- HTML/CSS
- Docker
- Git & GitHub

## Security Implementations
- Hashed passwords using Werkzeug
- Secure file names using secure_filename()
- Allowed file type validation
- X-Frame-Options header
- X-Content-Type-Options header
- Cache-Control header
- Role-based admin access

## Run Locally

```bash
pip install -r requirements.txt
python app.py
