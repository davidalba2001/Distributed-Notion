#dependencias
from src.utils import set_id
import socket

#operaciones chord
JOIN = 'join'
CONFIRM_FIRST = 'conf_first'
FIX_FINGER = 'fix_fing'
FIND_FIRST = 'fnd_first'
REQUEST_DATA = 'req_data'
CHECK_PREDECESOR = 'check_pred'
NOTIFY = 'notf'
UPDATE_PREDECESSOR = 'upt_pred'
UPDATE_FINGER = 'upd_fin'

#dirección de broadcast
BROADCAST_IP = '255.255.255.255' 

#operadores database
REGISTER = 'reg'
LOGIN = 'log'
ADD_CONTACT = 'add_cnt'
ADD_NOTE = 'add_not'
RECV_MSG = 'rec_msg'
RECV_NOTE = 'rec_not'
GET = 'get'

#nodos referentes a otros servidores
class NodeReference:
  def __init__(self, ip: str, port: int):
    self._id = set_id(ip)
    self._ip = ip
    self._port = port
    
  #enviar data 
  def _send_data(self, op: str, data=None) -> bytes:
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((self._ip, self._port))
        s.sendall(f'{op}|{data}'.encode('utf-8'))
        return s.recv(1024)
      
    except Exception as e:
      print(f"Error sending data: {e}")
      return b''
  
  ############################ INTERACCIONES CON LA DB #######################################
  #registrar un usuario
  def register(self, id: int, name: str, number: int) -> bytes:
    response = self._send_data(REGISTER, f'{id}|{name}|{number}')
    return response
  
  #logear a un usuario
  def login(self, id: int, name: str, number: int) -> bytes:
    response = self._send_data(LOGIN, f'{id}|{name}|{number}')
    return response
      
  #un usuario agreaga un contacto
  def add_contact(self, id: int, name: str) -> bytes:
    response = self._send_data(ADD_CONTACT, f'{id}|{name}')
    return response
  
  #una nota recibe un sms
  def recv_msg(self, id: int, note: str, username: int, msg: str) -> bytes:
    response = self._send_data(RECV_MSG, f'{id}|{note}|{username}|{msg}')
    return response
  
  #operaaciones get
  def get(self, id: int, endpoint: str):
    response = self._send_data(GET, f'{id}|{endpoint}')
    return response
  ############################################################################################
  
  ############################### OPERACIONES CHORD ##########################################
  #unir un nodo a la red
  def join(self, ip, port):
    response = self._send_data(JOIN, f'{ip}|{port}')
    return response
  
  #buscar el nodo 'first'
  def find_first(self):
    response = self._send_data(FIND_FIRST)
    return response
  
  #pedir data a mis conexiones
  def request_data(self, id: int):
    response = self._send_data(REQUEST_DATA, f'{id}')
    return response
  ############################################################################################ 
  
  @property
  def id(self):
    return self._id
  
  @property
  def ip(self):
    return self._ip
  
  @property
  def port(self):
    return self._port
  
#enviar mensajes por broadcast a la red
class BroadcastRef(): 
  def __init__(self, port: int):
    self._port = port
     
  #enviar data
  def _send_data(self, op: str, data=None) -> bytes:
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(f'{op}|{data}'.encode('utf-8'), (BROADCAST_IP, self._port))
    
    except Exception as e:
      print(f"Error sending data: {e}")
      return b''
  
  #mandar una solicitud a todos los nodos para unirme
  def join(self):
    self._send_data(JOIN)
  
  #mandar una solicitud a todos los nodos para que actualicen sus finger tables
  def fix_finger(self):
    self._send_data(FIX_FINGER)
    
  #notificar a todos los nodos de la caida de un nodo
  def notify(self, id: str):
    self._send_data(NOTIFY, id)
    
  #decirle a los nodos que actualicen su finger table debido a la caida de un nodo
  def update_finger(self, id: str):
    self._send_data(UPDATE_FINGER, id)
    
#enviar data a los servidores udp
def send_data(op: str, ip: str, port: str, data=None):
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
      s.sendto(f'{op}|{data}'.encode('utf-8'), (ip, port))
    
  except Exception as e:
    print(f"Error sending data: {e}")
    return b''
    