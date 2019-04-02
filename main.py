from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask import g
from flask_wtf import CsrfProtect

from config import DevelopmentConfig
from models import db
from models import User

import forms
import json

# Instancia 
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect()

# 404
@app.errorhandler(404)
def page_not_found( e ):
   return render_template('404.html'), 404 

# Decorador
@app.before_request
def before_request():
   if 'username' not in session and request.endpoint in ['comment']:
      return redirect(url_for('login'))
   elif 'username' in session and request.endpoint in ['login', 'register']:
      return redirect(url_for('index'))


@app.after_request
def after_request(response):
   return response


# Rutas
@app.route('/')
def index():
   if 'username' in session:
      username = session['username']
      print username

   title = 'My Index'
   return render_template('index.html', title = title)


@app.route('/login', methods = ['GET', 'POST']) 
def login():
   login_form = forms.LoginForm(request.form)
   if request.method == 'POST' and login_form.validate():
      #Mensaje Flash
      username             = login_form.username.data
      password             = login_form.password.data

      #select * from users where username = username limit 1
      user = User.query.filter_by(username = username).first()
      if user is not None and user.verify_password(password):
         success_message      = 'Bienvenido {}'.format(username)
         flash(success_message)
         session['username'] = username
         return redirect(url_for('index'))
      else:
         error_message= 'Usuario o Password no validos'
         flash(error_message)

      #Mensaje de session
      session['username']  = login_form.username.data 

   return render_template('login.html', form = login_form)


@app.route('/logout')
def logout():
   if 'username' in session:
      session.pop('username')
   return redirect(url_for('login'))


@app.route('/cookie')
def cookie():
   response = make_respons( render_template('cookie.html') )
   response.set_cookie('custome_cookie', 'Camilo')
   return response


@app.route('/comment', methods = ['GET', 'POST']) 
def comment():
   comment_form = forms.CommentForm(request.form)
   if request.method == 'POST' and comment_form.validate():
      
      print comment_form.username.data
      print comment_form.email.data
      print comment_form.comment.data
   else:
      print "Error en el Formulario"

   title = 'Curso Flask'
   return render_template('comment.html', title = title, form = comment_form)


@app.route('/ajax-login', methods =  ['POST'])
def ajax_login():
   username = request.form['username']
   response = {'status':200, 'username': username, 'id':1}
   return json.dumps(response)


@app.route('/register', methods = ['GET', 'POST'])
def register():
   register_form = forms.RegisterUserForm(request.form)
   if request.method == 'POST' and register_form.validate():

      user = User( register_form.username.data,
                   register_form.password.data,
                   register_form.email.data )

      db.session.add(user)
      db.session.commit()

      success_message = 'Usuario registrado en nuestra Base de Datos'
      flash(success_message)
   else:
      print "Error en el Formulario Register"

   return render_template('register.html', form = register_form)













if __name__ == '__main__':
   csrf.init_app(app)
   db.init_app(app)

   with app.app_context():
      db.create_all()

   app.run( port = 5000 )