from flask import Flask,request,make_response,render_template,redirect,session,url_for,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail,Message
from threading import Thread
import os
app=Flask(__name__)
# start of email server configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[Flasky]'
app.config['FLASKY_MAIL_SENDER']='Flasky Admin <flasky@example.com>'
app.config['FLASK_ADMIN']=os.environ.get('FLASKY_ADMIN')
mail=Mail(app)
# end of email server configuration

#start sqllite database configuration
base_dir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(base_dir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
migrate=Migrate(app,db)
#end sqlite database configuration
app.config['SECRET_KEY']='this is my secret key'
boostrap=Bootstrap(app)
moment=Moment(app)
def send_aync_email(app,meg):
 with app.app_context():
   mail.send(msg)
class User(db.Model):
 __tablename__='users'
 id=db.Column(db.Integer,primary_key=True)
 username=db.Column(db.String(64),unique=True)
 role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
 def __repr__(self):
  return '<User %r>'%self.username
class Role(db.Model):
 __tablename__='roles'
 id=db.Column(db.Integer,primary_key=True)
 name=db.Column(db.String(64),unique=True)
 users=db.relationship('User',backref='role')
 def __repr__(self):
  return '<Role %r>'%self.name

def send_email(to,subject,template,**kwargs):
 msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
 msg.body=render_template(template+'.txt',**kwargs)
 msg.html=render_template(template+'.html',**kwargs)
 mail.send(msg)
@app.route('/',methods=['GET','POST'])
def index():
 name=None
 form=PersonForm()
 if form.validate_on_submit():
  user=User.query.filter_by(username=form.name.data).first()
  if user is None:
   user=User(username=form.name.data)
   db.session.add(user)
   #db.session.commit()
   session['known']=False
   if app.config['FLASKY_ADMIN']:
    send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
  else:
   session['known']=True
  session['name']=form.name.data
  return redirect(url_for('index'))
 return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))
@app.route('/detail')
def detail():
 return render_template('detail.html',name=session.get('name'))
@app.route('/user/<name>')
def user(name):
  people=[Person('mohammed','male'),Person('ali','male'),Person('amina','female')]
  return render_template('user.html',name=name)
@app.route('/')
def agent():
 user_agent=request.headers.get('User-Agent')
 response=make_response('<h1>This document carries a cookie!</h1>')
 response.set_cookie('answer','42')
 return response
@app.route('/user/<id>')
def get_user(id):
 user=load_user(id)
@app.errorhandler(400)
def page_not_found(e):
 return render_template('400.html'),400
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html')
 if not user:
  abort(404)

@app.route('/user/<int:id>/<name>')
def hello(id,name):
 return '<h1>Hello changed {} {}</h1>'.format(id,name)
def about_us():
 return '<h1>About US </h1>'
app.add_url_rule('/about','about_us',about_us)
@app.shell_context_processor
def make_shell_context():
 return dict(db=db, User=User, Role=Role)
class Person():
 def __init__(self,name,gender):
  self.name=name
  self.gender=gender
class PersonForm(FlaskForm):
 name=StringField('What is your name',validators=[DataRequired()])
 submit=SubmitField('Submit')


if __name__=='__main__':
 app.run(debug=True)


