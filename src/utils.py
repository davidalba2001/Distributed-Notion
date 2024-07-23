#dependencias
import hashlib
import os
import shutil
import socket

#hashear la data
def set_id(data: str):
  return int(hashlib.sha1(data.encode()).hexdigest(), 16)

#optener mi ip
def get_ip() -> str:
  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    try:
        #usamos una IP arbitraria que no se encuentra en nuestra red
        s.connect(('10.254.254.254', 1))
        ip_local = s.getsockname()[0]
        
    except Exception:
        ip_local = '127.0.0.1'
        
    return str(ip_local)

#resetear una carpeta
def create_folder(path: str):
  if os.path.exists(path):
    rem_dir(path)
    
  os.makedirs(path)

#borrar folder
def rem_dir(dir: str):
  if os.path.exists(dir):
    shutil.rmtree(dir)