from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from WebSite.models import User

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=12)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Contraseña', validators=[DataRequired()])

    confirm_password = PasswordField('Confirmación de contraseña', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Registrate!')

    # Métodos para la validación

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Ya existe alguien llamado así. Por favor elige otro nickname.')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Ese correo ya se encuentra registrado.')

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Contraseña', validators=[DataRequired()])

    remember = BooleanField('Mantener sesión iniciada')

    submit = SubmitField('Ingresar')

class UpdateAccountForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=12)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Cambiar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Guardar Cambios')

    def validate_username(self, username):

        if username.data != current_user.username:
            
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError('Ya existe alguien llamado así. Por favor elige otro nombre.')

    def validate_email(self, email):

        if email.data != current_user.email:

            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('Ese correo ya se encuentra registrado.')
