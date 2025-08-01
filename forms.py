# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DecimalField, DateField, BooleanField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, URL
from wtforms.widgets import CheckboxInput, ListWidget


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Admin User')


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])


class MultiCheckboxField(SelectField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class EmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    
    department = SelectField('Department', 
                            choices=[('IT', 'Information Technology'),
                                   ('HR', 'Human Resources'),
                                   ('Finance', 'Finance'),
                                   ('Marketing', 'Marketing'),
                                   ('Sales', 'Sales'),
                                   ('Operations', 'Operations')],
                            validators=[DataRequired()])
    
    position = StringField('Position', validators=[DataRequired(), Length(max=50)])
    salary = DecimalField('Salary', validators=[DataRequired(), NumberRange(min=0)])
    hire_date = DateField('Hire Date', validators=[DataRequired()])
    
    gender = SelectField('Gender', 
                        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                        validators=[DataRequired()])
    
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=500)])
    skills = StringField('Skills (comma-separated)', validators=[Optional()])
    is_active = BooleanField('Active Employee', default=True)
    image = FileField('Profile Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    website = StringField('Website', validators=[Optional(), URL()])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=1000)])