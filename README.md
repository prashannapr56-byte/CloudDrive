# ☁️ CloudDrive

A secure cloud file storage web application built with **Flask**, **MySQL**, and **AWS S3**.

## Features
- 🔐 User Registration & Login
- 📤 Upload files to AWS S3
- 📋 View your uploaded files
- 🗑️ Delete files from AWS S3
- 🌙 Dark mode UI

## Tech Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** MySQL
- **Cloud Storage:** AWS S3 (boto3)
- **Environment:** Ubuntu (WSL2), Python 3.14

## Setup

### 1. Clone the repository
\\ash
git clone https://github.com/YOUR_USERNAME/CloudDrive.git
cd CloudDrive
\
### 2. Create virtual environment
\\ash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\
### 3. Configure environment variables
\\ash
cp .env.example .env
# Edit .env with your actual values
\
### 4. Set up MySQL database
\\sql
CREATE DATABASE clouddrive;
CREATE USER 'clouduser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON clouddrive.* TO 'clouduser'@'localhost';
\
### 5. Run the app
\\ash
python app.py
\
Open your browser at **http://localhost:5000**
