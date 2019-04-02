from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import validators

from models import User

def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe estar vacio.')


class CommentForm(Form):

    username    =  StringField('Nombre de Usuario', [
                                    validators.Required(message='El Nombre de Usuario es requerido!'),
                                    validators.length(min=4 ,max=25, message='Ingrese un Nombre de Usuario valido!')
                                ])

    email       =  EmailField('Correo Electronico',[
                                    validators.Required(message='El Email  es requerido!'),
                                    validators.Email(message='Ingrese un Email valido!')
                                ])
    comment     =  TextField('Comentario')

    honeypot    =  HiddenField('', [length_honeypot])


class LoginForm(Form):
    
    username    =  StringField('Nombre de Usuario', [
                                    validators.Required(message='El Nombre de Usuario es requerido!'),
                                    validators.length(min=4 ,max=25, message='Ingrese un Nombre de Usuario valido!')
                                ])

    password    =  PasswordField('Password', [
                                    validators.Required('El Password rd requerido!')
                                ])


class RegisterUserForm(Form):
    
    username    =  StringField('Nombre de Usuario', [
                                    validators.Required(message='El Nombre de Usuario es requerido!'),
                                    validators.length(min=4 ,max=25, message='Ingrese un Nombre de Usuario valido!')
                                ])

    email       =  EmailField('Correo Electronico',[
                                    validators.Required(message='El Email  es requerido!'),
                                    validators.Email(message='Ingrese un Email valido!'),
                                    validators.length(min=4 ,max=50, message='Ingrese un Email valido!')
                                ])

    password    =  PasswordField('Password', [
                                    validators.Required('El Password es requerido!')
                                ])

    def validate_username(form, field):
        username    = field.data
        user        = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('El Nombre de Usuario ya se encuentra registrado!')
