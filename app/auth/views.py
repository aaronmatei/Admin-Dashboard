from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee, generate_confirmation_token, generate_password_hash
from app import bcrypt, jwt


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            company='',
                            department='',
                            role='',
                            password=bcrypt.generate_password_hash(
                                request.form['password']).decode('utf-8')
                            )

        employee.save()
        token = generate_confirmation_token(employee.email)
        flash('You have successfully registered! You may now login.', 'success')
        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    # if current_user.is_authenticated:
    #     return redirect(url_for('home.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.objects.get(email=form.email.data)

        # if employee is not None and employee.verify_password(
        #         form.password.data):
        if employee is not None and bcrypt.check_password_hash(employee.password, form.password.data):
            user_obj = Employee(username=employee['username'])

            # log employee in
            login_user(user_obj)
            if employee.is_admin:
                print(employee.is_admin)

                return redirect(url_for('home.admin_dashboard'))
            else:
                # redirect to the dashboard page after login
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.', 'success')

    # redirect to the login page
    return redirect(url_for('auth.login'))
