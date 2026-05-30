# Secure Student Resource Sharing Portal

# EduVault

EduVault is a cloud-based secure educational resource management platform developed using Flask and deployed on AWS following DevSecOps principles.

The platform enables users to securely access educational resources while administrators manage users and resources through a role-based dashboard.

## Features

- User Registration and Login
- Role-Based Access Control
- Admin Dashboard
- Educational Resource Management
- Dockerized Deployment
- HTTPS using Let's Encrypt
- Nginx Reverse Proxy
- AWS CloudWatch Monitoring
- CloudWatch Alarms
- Automated Backup Script
- Amazon S3 Backup Storage
- GitHub Actions CI/CD Pipeline
- Password Hashing
- Security Headers
- API Rate Limiting

## Technology Stack

Frontend:
- HTML
- CSS
- Bootstrap
- JavaScript

Backend:
- Python Flask

Database:
- SQLite

Cloud:
- AWS EC2
- AWS S3
- AWS CloudWatch

DevOps:
- Docker
- Docker Compose
- GitHub Actions

Security:
- Nginx
- UFW Firewall
- Let's Encrypt SSL

## Security Features

- HTTPS SSL/TLS Encryption
- Password Hashing
- SQL Injection Protection
- XSS Protection
- Security Headers
- SSH Hardening
- UFW Firewall
- API Rate Limiting

## Monitoring

- AWS CloudWatch Metrics
- CloudWatch Alarms
- Docker Logs
- Nginx Logs

 ## Backup Strategy

Automated backup scripts generate compressed backups and store them in Amazon S3.

## Run Locally

```bash
pip install -r requirements.txt
python app.py
