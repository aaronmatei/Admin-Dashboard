# Forms for admin blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department, Role, Company

ALLDEPARTMENTS = [(department.id, department.name)
                  for department in Department.objects()]
ALLCOMPANIES = [
    (company.id, company.name) for company in Company.objects()]
ALLROLES = [(role.id, role.name) for role in Role.objects()]


class CompanyForm(FlaskForm):
    """
    Form for admin to add or edit a company
    """
    name = StringField('Company Name', validators=[
                       DataRequired(), Length(min=4, max=50)])
    description = StringField('Description', validators=[
                              DataRequired(), Length(min=4, max=50)])
    address = StringField('Address', validators=[DataRequired()])
    person_contact = StringField(
        'Contact Person Phone', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Contact Person Email', validators=[
                        DataRequired(), Email(), Length(min=4, max=50)])
    first_name = StringField('Contact Person First Name',
                             validators=[DataRequired(), Length(min=4, max=50)])
    last_name = StringField('Contact Person Last Name',
                            validators=[DataRequired(), Length(min=4, max=50)])

    submit = SubmitField('Submit')


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    # company = SelectField('Company', validators=[
    #                       DataRequired], choices=ALLCOMPANIES)
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    # department = QuerySelectField(query_factory=lambda: Department.objects(),
    #                               get_label="name")
    # role = QuerySelectField(query_factory=lambda: Role.objects(),
    #                         get_label="name")

    company = SelectField('Company', choices=ALLCOMPANIES)
    department = SelectField('Department', choices=ALLDEPARTMENTS)
    role = SelectField(
        'Role', choices=ALLROLES)

    submit = SubmitField('Submit')
