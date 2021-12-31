
import socket





username = 'Adminstrator'
password = '2292'
server_ip = '192.168.178.106'
system_name = 'pi'
share_name = r'\\pi\d$'





HOST = '\\pi'
PORT = 445
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(s.getsockname())
    print(s.getpeername())
    #print(s.proto)
    print(dir(s))
    s.close()
    




