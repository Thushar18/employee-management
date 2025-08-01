from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid
import secrets
from dotenv import load_dotenv
load_dotenv()
from config import Config
from models import db, User, Employee
from forms import LoginForm, RegisterForm, ForgotPasswordForm, EmployeeForm

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Generate session token for state management
            session_token = user.generate_session_token()
            db.session.commit()
            login_user(user)
            session['user_token'] = session_token
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()
        if existing_user:
            flash('Username or email already exists', 'error')
            return render_template('register.html', form=form)

        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=form.is_admin.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Generate temporary password
            temp_password = secrets.token_urlsafe(12)
            user.set_password(temp_password)
            db.session.commit()

            # Send email with plain text password (as per requirements)
            try:
                msg = Message(
                    'Password Reset - Employee Management System',
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[user.email]
                )
                msg.body = f'''
                Hello {user.username},

                Your password has been reset. Here are your new login credentials:

                Username: {user.username}
                Password: {temp_password}

                Please login and change your password immediately.

                Best regards,
                Employee Management System
                '''
                mail.send(msg)
                flash('Password reset email sent!', 'success')
            except Exception as e:
                flash('Error sending email. Please try again.', 'error')
        else:
            flash('Email not found', 'error')
    return render_template('forgot_password.html', form=form)


@app.route('/logout')
@login_required
def logout():
    # Clear session token
    current_user.session_token = None
    db.session.commit()
    session.clear()
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    # Check session token for additional security
    if 'user_token' not in session or session['user_token'] != current_user.session_token:
        flash('Session expired. Please login again.', 'warning')
        return redirect(url_for('login'))

    page = request.args.get('page', 1, type=int)
    search_name = request.args.get('search_name', '')
    search_phone = request.args.get('search_phone', '')

    query = Employee.query

    # Apply search filters
    if search_name:
        query = query.filter(Employee.first_name.contains(search_name))
    if search_phone:
        query = query.filter(Employee.phone.contains(search_phone))

    employees = query.paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('dashboard.html', employees=employees,
                         search_name=search_name, search_phone=search_phone)


@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        # Handle file upload
        image_filename = None
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to prevent conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                image_filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        employee = Employee(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            department=form.department.data,
            position=form.position.data,
            salary=form.salary.data,
            hire_date=form.hire_date.data,
            gender=form.gender.data,
            address=form.address.data,
            skills=form.skills.data,
            is_active=form.is_active.data,
            image_filename=image_filename,
            website=form.website.data,
            notes=form.notes.data,
            created_by=current_user.id
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_employee.html', form=form)


@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        # Handle file upload
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                image_filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                employee.image_filename = image_filename

        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.email = form.email.data
        employee.phone = form.phone.data
        employee.department = form.department.data
        employee.position = form.position.data
        employee.salary = form.salary.data
        employee.hire_date = form.hire_date.data
        employee.gender = form.gender.data
        employee.address = form.address.data
        employee.skills = form.skills.data
        employee.is_active = form.is_active.data
        employee.website = form.website.data
        employee.notes = form.notes.data
        employee.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_employee.html', form=form, employee=employee)


@app.route('/delete_employee/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/api/employees')
@login_required
def api_employees():
    """API endpoint for employee data"""
    employees = Employee.query.all()
    return jsonify([{
        'id': emp.id,
        'first_name': emp.first_name,
        'last_name': emp.last_name,
        'email': emp.email,
        'phone': emp.phone,
        'department': emp.department,
        'position': emp.position,
        'is_active': emp.is_active
    } for emp in employees])


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        # Create upload folder
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created.")

        # Create default users
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            new_admin = User(username='admin', email='admin@jalaacademy.com', is_admin=True)
            new_admin.set_password('admin123')
            db.session.add(new_admin)
            db.session.commit()
            print("✓ Admin user created: admin/admin123")

        user = User.query.filter_by(username='user').first()
        if not user:
            new_user = User(username='user', email='user@jalaacademy.com', is_admin=False)
            new_user.set_password('user123')
            db.session.add(new_user)
            db.session.commit()
            print("✓ Regular user created: user/user123")

    # Run the app
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)