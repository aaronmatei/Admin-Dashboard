# Views for admin blueprint
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import admin
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm, CompanyForm
from .. import db
from ..models import Department, Role, Employee, Company


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    # if not current_user.is_admin:
    #     abort(403)
    if current_user.username != 'Admin':
        abort(403)


# Department Views


@admin.route('/companies/departments/<comp_id>', methods=['GET', 'POST'])
@login_required
def list_departments(comp_id):
    """
    List all departments
    """
    check_admin()
    form = DepartmentForm()
    this_company = Company.objects.get(id=comp_id)

    departments = Department.objects(company=this_company.name)

    if request.method == "POST":  # and form.validate():
        department = Department(name=form.name.data,
                                company=this_company.name,
                                description=form.description.data)
        # add department to the database
        department.save()
        flash('You have successfully added a new department.')
        # try:
        #     # add department to the database
        #     department.save()
        #     flash('You have successfully added a new department.')
        # except:
        #     # in case department name already exists
        #     flash('Error: department name already exists.')

    return render_template('admin/companies/departments/departments.html',
                           departments=departments, comp_id=this_company.id, company_name=this_company.name, form=form, title="Departments")


@admin.route('/companies/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()

    if request.method == "POST":  # and form.validate():
        company_name = Company.objects.get(id=form.company.data)
        department = Department(name=form.name.data,
                                company=company_name.name,
                                description=form.description.data)

        try:
            # add department to the database

            department.save()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return redirect(url_for('admin.list_departments'))
    # return render_template('admin/companies/departments/department.html', action="Add",
    #                        add_department=add_department, form=form,
    #                        title="Add Department")


@admin.route('/companies/departments/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.objects.get(id=id)
    form = DepartmentForm(obj=department)
    this_company = Company.objects.get(name=department.company)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        # department.company = form.company.data

        department.save()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments', comp_id=this_company.id))

    form.description.data = department.description
    form.name.data = department.name
    # form.company.data = department.company

    # return redirect(url_for('admin.list_departments'))
    return render_template('admin/companies/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/companies/departments/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.objects.get(id=id)
    this_company = Company.objects.get(name=department.company)
    department.delete()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments', comp_id=this_company.id))

    return render_template(title="Delete Department")


# company views
@admin.route('/companies', methods=['GET', 'POST'])
@login_required
def list_companies():
    """
    List all companies
    """
    check_admin()

    companies = Company.objects()
    departments = Department.objects()

    return render_template('admin/companies/companies.html',
                           companies=companies, departments=departments, title="Departments")


@admin.route('/companies/add', methods=['GET', 'POST'])
@login_required
def add_company():
    """
    Add a company to the database
    """
    check_admin()

    add_company = True

    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(name=form.name.data,
                          address=form.address.data,
                          description=form.description.data,
                          person_contact=form.person_contact.data,
                          email=form.email.data,
                          first_name=form.first_name.data,
                          last_name=form.last_name.data)
        try:
            # add company to the database
            company.save()
            flash('You have successfully added a new Company.')
        except:
            # in case department name already exists
            flash('Error: That Company name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_companies'))

    # load department template
    return render_template('admin/companies/company.html', action="Add",
                           add_company=add_company, form=form,
                           title="Add Company")


@admin.route('/companies/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_company(id):
    """
    Edit a company details
    """
    check_admin()

    add_company = False

    company = Company.objects.get(id=id)
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        company.name = form.name.data
        company.description = form.description.data
        company.address = form.address.data
        company.save()
        flash('You have successfully edited the Company.')

        # redirect to the departments page
        return redirect(url_for('admin.list_companies'))

    form.description.data = company.description
    form.name.data = company.name
    form.address.data = company.address
    return render_template('admin/companies/company.html', action="Edit",
                           add_company=add_company, form=form,
                           company=company, title="Edit Company")


@admin.route('/companies/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_company(id):
    """
    Delete a company from the database
    """
    check_admin()

    company = Company.objects.get(id=id)
    company.delete()
    flash('You have successfully deleted the company.')

    # redirect to the departments page
    return redirect(url_for('admin.list_companies'))

    return render_template(title="Delete Company")


# Role Views

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.objects()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            role.save()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.objects.get(id=id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        role.save()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.objects.get(id=id)
    role.delete()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.objects()
    departments = Department.objects()
    roles = Role.objects()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.objects.get(id=id)

    # prevent admin from being assigned a department or role
    # if employee.is_admin:
    #     abort(403)
    if employee.username == 'Admin':
        abort(403)

    form = EmployeeAssignForm(obj=employee)

    # if form.validate_on_submit():
    if request.method == 'POST':
        department = Department.objects.get(id=form.department.data)
        company = Company.objects.get(id=form.company.data)
        role = Role.objects.get(id=form.role.data)
        # employee.department_name = form.department.name
        # employee.role_name = form.role.data
        # employee.company_name = form.role.data

        employee.update(set__department=department.name, set__company=company.name, set__role=role.name)

        flash('Assignment successful.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')
