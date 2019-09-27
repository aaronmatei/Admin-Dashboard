from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeSerializer
from flask_mail import Mail, Message
from flask import current_app as app


from app import db, login_manager, jwt, mail


class Department(db.Document):
    """
    Create a Department table
    """

    name = db.StringField(max_length=30, unique=True)
    description = db.StringField(max_length=250)
    employees = db.ListField(db.ReferenceField('Employee'))

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Document):
    """
    Create a Role table
    """

    name = db.StringField(max_length=250, unique=True)
    description = db.StringField(max_length=250)
    employees = db.ListField(db.ReferenceField('Employee'))

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Employee(UserMixin, db.Document):
    """
    Create an Employee table
    """

    email = db.StringField(unique=True)
    username = db.StringField(max_length=20)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    password = db.StringField()
    hashed_password = db.StringField()
    department_id = db.ReferenceField(Department)
    role_id = db.ReferenceField(Role)
    is_admin = db.BooleanField(default=False)

    # @property
    # def password(self):
    #     """
    #     Prevent pasword from being accessed
    #     """
    #     raise AttributeError('password is not a readable attribute.')
    # @password.setter
    # def password(self, password):
    #     """
    #     Set password to a hashed password
    #     """
    #     self.password_hash = generate_password_hash(password)
    # def verify_password(self, password):
    #     """
    #     Check if hashed password matches actual password
    #     """
    #     return check_password_hash(self.hashed_password, password)

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(username):
    # print(username)
    user_name = Employee.objects.get(username=username)
    if not user_name:
        return None
    return Employee(username=user_name['username'])


def generate_confirmation_token(email):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'],
                                 max_age=expiration)
    except:
        return False
    return email


def send_confirmation_email(email):
    confirm_serializer = URLSafeSerializer(app.config['SECRET_KEY'])


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


# def is_Admin(username):
#     if Employee.objects.get(username == 'Admin'):
#         return True
#     return False
