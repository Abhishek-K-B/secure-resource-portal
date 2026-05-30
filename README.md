# Secure Student Resource Sharing Portal

# EduVault

## Project Overview

EduVault is a secure cloud-based educational resource management platform developed using Flask and deployed on Amazon Web Services (AWS) following DevSecOps principles.

The application enables users to securely access educational resources while allowing administrators to manage users and resources through a role-based administrative interface.

The project demonstrates the implementation of cloud infrastructure, cybersecurity controls, containerization, monitoring, automation, and CI/CD practices in a real-world deployment environment.

## Project Objectives

The primary objectives of this project are:

Develop a secure web application using Flask.
Deploy the application on AWS cloud infrastructure.
Implement DevSecOps best practices.
Secure application communication using HTTPS.
Implement role-based access control.
Containerize the application using Docker.
Configure automated CI/CD using GitHub Actions.
Implement monitoring using AWS CloudWatch.
Configure automated backup mechanisms.
Apply security controls to protect the application.
Key Features
User Features
User Registration
Secure User Login
Resource Access
Session Management
Secure Logout

## Administrator Features:

Administrative Dashboard
Resource Management
User Management
Access Control Management

## Security Features:

HTTPS Encryption (Let's Encrypt)
Password Hashing
Security Headers
SQL Injection Protection
Cross-Site Scripting (XSS) Protection
Rate Limiting
SSH Hardening
UFW Firewall Protection
Role-Based Access Control (RBAC)

## DevOps Features:

Docker Containerization
Docker Compose Deployment
GitHub Version Control
GitHub Actions CI/CD Pipeline
Automated Deployment Workflow

## Monitoring Features:

AWS CloudWatch Metrics
CloudWatch Alarms
Docker Logs
Nginx Logs
Health Monitoring

## Backup Features:

Automated Backup Script
Amazon S3 Backup Storage
Backup Verification

## Technology Stack:

## Frontend
HTML5
CSS3
Bootstrap
JavaScript
## Backend
Python
Flask Framework
## Database
SQLite
## Web Server
Nginx Reverse Proxy
## Containerization
Docker
Docker Compose
## Cloud Platform
Amazon Web Services (AWS)
## AWS Services Used
EC2
VPC
## Security Groups
Application Load Balancer
S3
CloudWatch
IAM
## CI/CD
GitHub Actions

## Architecture Overview:

Users
   │
   ▼
DuckDNS Domain
   │
HTTPS (Let's Encrypt)
   │
Application Load Balancer
   │
EC2 Ubuntu Server
   │
Nginx Reverse Proxy
   │
Dockerized Flask Application
   │
SQLite Database
   │
Backup Script
   │
Amazon S3

## Monitoring:
CloudWatch Metrics
CloudWatch Logs
CloudWatch Alarms

## Project Structure:
secure-resource-portal/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── backup.sh
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── admin.html
│
├── static/
│   ├── style.css
│
├── uploads/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
└── README.md

## Deployment Guide
  Step 1 – Clone Repository
git clone https://github.com/Abhishek-K-B/secure-resourse-portal.git
cd secure-resource-portal
  Step 2 – Install Docker
sudo apt update
sudo apt install docker.io -y
  Step 3 – Install Docker Compose
sudo apt install docker-compose -y
  Step 4 – Build Application
sudo docker-compose build
  Step 5 – Start Containers
sudo docker-compose up -d
  Step 6 – Verify Deployment
sudo docker ps

## Expected:

secure-resource-portal_web_1

Nginx Reverse Proxy Configuration:

Nginx is configured as a reverse proxy and forwards requests to the Flask application running inside Docker.

## Responsibilities:

HTTP Request Handling
HTTPS Termination
SSL Certificate Management
Reverse Proxy Routing
HTTPS Configuration

## HTTPS is implemented using:

DuckDNS
Let's Encrypt SSL Certificates
Nginx Reverse Proxy

## Benefits:

Encrypted Communication
Secure Authentication
Data Protection

## Security Implementation:
Password Hashing

User passwords are hashed before storage to protect credentials.

Role-Based Access Control

Two user roles are implemented:

Administrator
Manage Resources
Manage Users
Access Admin Dashboard
Standard User
View Resources
Access User Dashboard

## SQL Injection Protection

Input validation and parameterized database operations are used to prevent SQL Injection attacks.

## Cross-Site Scripting (XSS) Protection

User inputs are validated and sanitized to prevent malicious script execution.

## Security Headers:

## Implemented security headers:

X-Frame-Options
X-Content-Type-Options
Strict-Transport-Security
Rate Limiting

Flask-Limiter is configured to prevent brute-force attacks and excessive requests.

Example:

50 requests per hour
SSH Hardening

SSH access is restricted using:

My IP/32

## Benefits:

Prevents unauthorized SSH access
Reduces attack surface
UFW Firewall

Configured Rules:

22/tcp
80/tcp
443/tcp

## CI/CD Pipeline

GitHub Actions is used for continuous integration and deployment.

Workflow:

Code Push
     │
GitHub Actions
     │
Build Validation
     │
Docker Build
     │
Deployment

Benefits:

Automated Build Validation
Faster Deployment
Consistent Releases

Monitoring & Logging
AWS CloudWatch

## Configured Metrics:

CPU Utilization
NetworkIn
NetworkOut
CloudWatch Alarms

## Configured Alerts:

High CPU Usage
Infrastructure Monitoring

Docker Logs

Used for:

Application Monitoring
Error Detection
Troubleshooting
Health Checks

Application Load Balancer health checks:

/health
Backup Strategy

## Automated backup scripts generate compressed backups of:

Application Files
Database Files
Uploaded Resources

Example:

./backup.sh

## Future Enhancements

Multi-Factor Authentication (MFA)
Amazon RDS Integration
JWT Authentication
AWS WAF Integration
Auto Scaling
Kubernetes Deployment
Advanced Analytics Dashboard
Author

Abhishek K B

Marian College Kuttikkanam
```bash
pip install -r requirements.txt
python app.py
