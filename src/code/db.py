#dependencias
from src.utils import set_id
import os

#direccion de donde estoy
DB = f'{os.path.dirname(os.path.abspath(__file__))}/db'

#encontrar un usuario segun su id
def find_user(id: int) -> str:
  for user in os.listdir(f'{DB}'):
    if set_id(user) == id:
      return f'{DB}/{user}'

#objeto para encapsular la interaccion del usuario con la db
class DB:
  #registrar un usuario en la db
  @classmethod
  def register(cls, name: str, number: int) -> str:
    #verificar si esta en la db
    if os.path.exists(f'{DB}/{name}'):
      return 'Username already in use'
    
    with open(f'{DB}/{name}/number.txt', 'r') as f:
      if str(number) in f.read():
        return 'User already in exists'
   
    #agregar al nuevo usuario
    os.mkdir(f'{DB}/{name}')
    
    with open(f'{DB}/{name}/number.txt', 'w') as f:
     f.write(number)
    
    with open(f'{DB}/{name}/contacts.txt', 'w') as f:
      f.write('')
      
    with open(f'{DB}/{name}/notes.txt', 'w') as f:
      f.write('')
      
    return 'Succesful registration'
    
  #logear un usuario
  @classmethod
  def login(cls, name: str, number: int) -> str:
    #verificar si esta en la db
    if os.path.exists(f'{DB}/{name}'):
      with open(f'{DB}/{name}/number.txt', 'r') as f:
        if str(number) in f.read(): 
          return ''
        
    return 'User not registred'

  #agregar un contacto
  @classmethod
  def add_contact(cls, id: int, name: str) -> str:
    #referenciar el usuario segun el id
    user = find_user(id)
      
    #validar si el contacto ya existe
    with open(f'{user}/contacts.txt', 'r') as f:
      if str(name) in f.read():
        return 'Contact already exists'
      
    with open(f'{user}/contacts.txt', 'a') as f:
      f.write(f'{name}\n')
    
    return ''
   
  #agregar una nota
  @classmethod 
  def add_note(cls, id: int, name: str) -> str:
    #referenciar el usuario segun el id
    user = find_user(id)
    endpoint = user.split('/')[-1]
      
    #validar si la nota ya existe
    with open(f'{user}/notes.txt', 'r') as f:
      if f'{name} - {endpoint}' in f.read():
        return 'Note already exists'
      
    with open(f'{user}/notes.txt', 'a') as f:
      f.write(f'{name} - {endpoint}\n')
    
    return ''
  
  #compartir una nota
  def recv_note(cls, id: int, name: str, note: str):
    #referenciar el usuario segun el id
    user = find_user(id)
    
    #validar si la nota ya fue compartida
    with open(f'{user}/notes.txt', 'r') as f:
      if f'{note} - {name}' in f.read():
        return 'Note already shared'
      
    with open(f'{user}/notes.txt', 'a') as f:
      f.write(f'{note} - {name}\n')
    
    return ''
    
  #recibir un sms
  @classmethod
  def recv_msg(cls, id: int, note: str, name: str, msg: str) -> str:
    user = find_user(id)
    
    with open(f'{user}/{note}.txt', 'a') as f:
      f.write(f'[{name}]: {msg}\n')   
      
    with open(f'{user}/{note}.txt', 'r') as f:
      return f.read() 
  
  #get 
  @classmethod
  def get(cls, id: int, endpoint: str) -> str:
    #referenciar el usuario segun el id
    user = find_user(id)
    
    with open(f'{user}/{endpoint}.txt', 'r') as f:
      return f.read().strip()
      
      
      
    
  