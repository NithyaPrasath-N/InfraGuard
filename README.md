# 🛡️ InfraGuard – Infrastructure Drift Detection & Remediation Platform

## 📌 Overview

InfraGuard is a DevOps-focused infrastructure governance platform that detects configuration drift between Terraform-managed infrastructure and actual AWS resources. The platform provides a centralized dashboard for monitoring infrastructure health, identifying drift risks, and performing automated remediation using Terraform.

This project demonstrates Infrastructure as Code (IaC), cloud governance, drift detection, risk assessment, and automated remediation workflows.

---

## 🚀 Features

### Drift Detection

* Detects drift in AWS EC2 instances
* Detects drift in AWS S3 bucket configurations
* Detects drift in AWS Security Group rules
* Compares Terraform state with live AWS infrastructure

### Risk Assessment

* Assigns risk levels:

  * 🔴 Critical
  * 🟠 High
  * 🔵 Medium
  * 🟢 Low
* Calculates infrastructure risk score
* Displays overall infrastructure health status

### Dashboard

* Interactive web dashboard built with Flask
* Infrastructure health monitoring
* Risk distribution visualization
* Active drift findings table
* One-click infrastructure scanning

### Automated Remediation

* Terraform-based remediation
* Targeted resource remediation
* Remediation execution logs
* Automated infrastructure recovery

---

## 🏗️ Architecture

AWS Resources
↓
Drift Detection Engine
↓
Risk Analysis Engine
↓
MySQL Database
↓
Flask Dashboard
↓
Terraform Remediation Engine

---

## 🛠️ Technology Stack

### Cloud

* AWS EC2
* AWS S3
* AWS Security Groups

### Infrastructure as Code

* Terraform

### Backend

* Python

### Web Framework

* Flask

### Database

* MySQL

### Frontend

* HTML
* CSS
* Bootstrap
* Chart.js

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
InfraGuard/
│
├── drift_detector/
│   ├── app.py
│   ├── db.py
│   ├── detect_drift.py
│   ├── ec2_detector.py
│   ├── s3_detector.py
│   ├── sg_detector.py
│   ├── risk_engine.py
│   ├── remediation_engine.py
│   ├── terraform_executor.py
│   ├── templates/
│   └── static/
│
├── terraform/
│   ├── main.tf
│   ├── provider.tf
│   └── terraform.lock.hcl
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/NithyaPrasath-N/InfraGuard.git
cd InfraGuard
```

### Install Dependencies

```bash
pip install flask
pip install boto3
pip install mysql-connector-python
```

### Configure AWS Credentials

```bash
aws configure
```

### Configure MySQL Database

Create database:

```sql
CREATE DATABASE infraguard;
```

### Run Application

```bash
cd drift_detector
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🔍 Workflow

### Drift Detection

1. Scan Infrastructure
2. Compare Terraform State with AWS
3. Detect Configuration Drift
4. Store Findings in MySQL
5. Display Findings on Dashboard

### Remediation

1. Select Drift Finding
2. Review Recommendation
3. Confirm Remediation
4. Execute Terraform Apply
5. Restore Infrastructure State
6. Re-scan Infrastructure

---

## 📊 Dashboard Capabilities

* Infrastructure Health Monitoring
* Risk Score Calculation
* Risk Distribution Visualization
* Active Drift Findings
* Remediation Management
* Scan History Tracking

---

## 🎯 Example Drift Scenarios

### EC2 Drift

* Instance type changed manually

### S3 Drift

* Bucket versioning disabled

### Security Group Drift

* Unauthorized inbound ports opened


---

## ⭐ Project Goal

InfraGuard was developed to demonstrate real-world DevOps practices including Infrastructure as Code, cloud governance, drift detection, risk assessment, and automated remediation in AWS environments.
