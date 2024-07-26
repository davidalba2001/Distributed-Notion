#dependencias
from flask import redirect, url_for, render_template, flash, request
from src.app.auth import auth, server
from src.app.auth.forms import *
from src.utils import set_id

#ruta del logear un usuario
@auth.route('/', methods=['GET', 'POST'])
def login():
  form = Login()
  context = {'form': form}
  
  if form.validate_on_submit():
    username = form.username.data
    number = form.number.data
    response = server.login(set_id(username), username, int(number))
    
    if response == 'User not registred':
      return render_template('login.html', **context)
    
    return redirect(url_for('auth.homepage', id=set_id(username), my_name=username))
  
  return render_template('login.html', **context)
  
#ruta de registrar
@auth.route('/register', methods=['GET', 'POST'])
def register():
  form = Register()
  context = {'form': form}
  
  if form.validate_on_submit():
    username = form.username.data
    number = form.number.data
    response = server.register(set_id(username), username, int(number))
  
    if response == 'User already exists':
      return render_template('register.html', **context)
    
    return redirect(url_for('auth.homepage', id=set_id(username), my_name=username))
  
  return render_template('register.html', **context)

#ruta de la homepage
@auth.route('/homepage')
def homepage():
  id = int(request.args.get('id'))
  my_name = request.args.get('my_name')
  data = server.get(id, 'notes')
  parse_data = data.split('\n')
  context = {
    'notes': [note for note in parse_data if note != ''],
    'id': id,
    'my_name': my_name
    } 
  return render_template('homepage.html', **context)

#rutar para agregar un contacto
@auth.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
  id = int(request.args.get('id'))
  my_name = request.args.get('my_name')
  form = AddContact()
  context = {
    'form': form,
    'id': id,
    'my_name': my_name
    }
  
  if form.validate_on_submit():
    username = form.name.data
    number = form.number.data
    server.register(set_id(username), username, int(number))
    response = server.add_contact(id, username, int(number))
  
    if response == 'Contact already exists':
      return render_template('add_contact.html', **context)
    
    return redirect(url_for('auth.contacts', id=id, my_name=my_name))
  
  return render_template('add_contact.html', **context)

#rutar para agregar una nota
@auth.route('/add_note', methods=['GET', 'POST'])
def add_note():
  id = int(request.args.get('id'))
  my_name = request.args.get('my_name')
  form = AddNote()
  context = {
    'form': form,
    'id': id,
    'my_name': 'sex'
    }
  
  if form.validate_on_submit():
    title = form.title.data
    response = server.add_note(id, title)
  
    if response == 'Note already exists':
      return render_template('add_note.html', **context)
    
    return redirect(url_for('auth.homepage', id=id, my_name=my_name))
  
  return render_template('add_note.html', **context)

