#dependencias
from src.code.db import DB
from src.utils import rem_dir, set_id, create_folder
import os

#manejar data
class HandleData():
  def __init__(self, id: int):
    self._garbage = []
    self._id = id
   
  #devolver data correspondiente a un usuario segun su id 
  def data(self, delete: bool, id=None) -> str:
    result = ''
    
    for user in os.listdir(DB):
      if id == None or (id < self._id and set_id(user) < id) or (id > self._id and set_id(user) > self._id):
        result += f'{user}'
        
        for file in os.listdir(f'{DB}/{user}'):
          with open(f'{DB}/{user}/{file}', 'r') as f:
            result += f'/{file}/{f.read()}'
  
        result += '|'
        self._garbage.append(f'{DB}/{user}')
      
    self._clean(delete)
    return result
  
  #crear data en la db
  @classmethod
  def create(cls, data: str):
    users = data.split('|')
    
    for user in users:
      if user != '':
        parse = user.split('/')
        create_folder(f'{DB}/{parse[0]}')
        info = parse[1:]
        
        for i in range(len(info)):
          if i % 2 != 0:
            continue
          
          with open(f'{DB}/{parse[0]}/{info[i]}', 'w') as f:
            f.write(info[i + 1])
  
  #eliminar data de la db almacenada en el garbage y reiniciar el garbage
  def _clean(self, delete: bool):
    if delete:
      for user in self._garbage:
        rem_dir(user)
    
    self._garbage = []
   