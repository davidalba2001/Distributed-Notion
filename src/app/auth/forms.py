#dependencias
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

#formulario de la vista 'register'
class Register(FlaskForm):
  username = StringField('username', validators=[DataRequired(), Length(1, 16, message='max 16 characters')])
  number = IntegerField('number', validators=[DataRequired(), NumberRange(min=10000000, message='invalid number (8 digits required)')])
  submit = SubmitField('sign up')
  
#formulario de la vista 'login'
class Login(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  number = IntegerField('number', validators=[DataRequired()])
  submit = SubmitField('sign in')
  
#formulario de la vista 'add_contact'
class AddContact(FlaskForm):
  username = StringField('name', validators=[DataRequired(), Length(1, 16, message='max 16 characters')])
  submit = SubmitField('add contact')
  
#formulario de la vista 'add_note'
class AddNote(FlaskForm):
  title = StringField('title', validators=[DataRequired(), Length(1, 16, message='max 16 characters')])
  submit = SubmitField('add note')
  
#formulario de la vista 'note'
class Note(FlaskForm):
  text = StringField('text', validators=[DataRequired()])
  submit = SubmitField('send')
  
#formulario de la vista share
class Share(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  submit = SubmitField('ok')