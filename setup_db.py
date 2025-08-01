#!/usr/bin/env python3
"""
Database setup script for Employee Management System
Run this script to initialize the database with tables and sample data.
"""
from app import app, db
from models import User, Employee
from datetime import date, datetime
import os

def create_sample_data():
    """Create sample users and employees for testing"""
    with app.app_context():
        # Create upload directory if it doesn't exist
        upload_folder = app.config.get('UPLOAD_FOLDER', 'static/uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Create all database tables
        db.create_all()
        
        print("✅ Database tables created successfully.")

        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@jalaacademy.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create regular user
            user = User(
                username='user',
                email='user@jalaacademy.com',
                is_admin=False
            )
            user.set_password('user123')
            db.session.add(user)
            
            db.session.commit()
            print("✓ Default users created:")
            print("  Admin: admin/admin123")
            print("  User: user/user123")
        else:
            print("⚠️ Admin user already exists. Skipping user creation.")

        # Check if any employees exist
        if Employee.query.count() == 0:
            # Create sample employees
            employees = [
                {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.doe@company.com',
                    'phone': '+1-555-0101',
                    'department': 'IT',
                    'position': 'Software Engineer',
                    'salary': 75000.00,
                    'hire_date': date(2023, 1, 15),
                    'gender': 'Male',
                    'address': '123 Main St, Anytown, USA 12345',
                    'skills': 'Python, JavaScript, SQL, React',
                    'is_active': True,
                    'website': 'https://johndoe.dev',
                    'notes': 'Excellent problem-solving skills and team player.',
                    'created_by': 1  # Admin user
                },
                {
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'email': 'jane.smith@company.com',
                    'phone': '+1-555-0102',
                    'department': 'HR',
                    'position': 'HR Manager',
                    'salary': 65000.00,
                    'hire_date': date(2022, 6, 10),
                    'gender': 'Female',
                    'address': '456 Oak Ave, Somewhere, USA 67890',
                    'skills': 'Communication, Leadership, Policy Development',
                    'is_active': True,
                    'notes': 'Strong leadership skills and excellent with employee relations.',
                    'created_by': 1
                },
                {
                    'first_name': 'Mike',
                    'last_name': 'Johnson',
                    'email': 'mike.johnson@company.com',
                    'phone': '+1-555-0103',
                    'department': 'Finance',
                    'position': 'Financial Analyst',
                    'salary': 60000.00,
                    'hire_date': date(2023, 3, 20),
                    'gender': 'Male',
                    'address': '789 Pine St, Elsewhere, USA 11111',
                    'skills': 'Excel, Financial Modeling, Data Analysis',
                    'is_active': True,
                    'notes': 'Detail-oriented with strong analytical skills.',
                    'created_by': 1
                },
                {
                    'first_name': 'Sarah',
                    'last_name': 'Wilson',
                    'email': 'sarah.wilson@company.com',
                    'phone': '+1-555-0104',
                    'department': 'Marketing',
                    'position': 'Marketing Specialist',
                    'salary': 55000.00,
                    'hire_date': date(2023, 8, 5),
                    'gender': 'Female',
                    'address': '321 Elm St, Nowhere, USA 22222',
                    'skills': 'Social Media, Content Creation, SEO',
                    'is_active': True,
                    'website': 'https://sarahwilsonmarketing.com',
                    'notes': 'Creative and results-driven marketing professional.',
                    'created_by': 1
                },
                {
                    'first_name': 'David',
                    'last_name': 'Brown',
                    'email': 'david.brown@company.com',
                    'phone': '+1-555-0105',
                    'department': 'Sales',
                    'position': 'Sales Representative',
                    'salary': 50000.00,
                    'hire_date': date(2023, 5, 12),
                    'gender': 'Male',
                    'address': '654 Maple Dr, Anywhere, USA 33333',
                    'skills': 'Sales, Customer Relations, CRM Software',
                    'is_active': False,
                    'notes': 'On leave for personal reasons.',
                    'created_by': 1
                }
            ]
            
            for emp_data in employees:
                employee = Employee(**emp_data)
                db.session.add(employee)
                
            db.session.commit()
            print(f"✓ Created {len(employees)} sample employees")
        else:
            print("⚠️ Sample employees already exist. Skipping.")

        # Final status
        total_users = User.query.count()
        total_employees = Employee.query.count()
        print("✓ Database setup completed successfully!")
        print(f"✓ Total users in database: {total_users}")
        print(f"✓ Total employees in database: {total_employees}")

if __name__ == '__main__':
    create_sample_data()