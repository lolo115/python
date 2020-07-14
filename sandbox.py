from paramiko import SSHClient
from scp import SCPClient
import os

with open("text.txt",'w+') as f:
    f.write("coucou Pierrot \n")

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname='192.168.99.100', username='laurent', password='laurent')

scp = SCPClient(ssh.get_transport())
scp.put(files=["text.txt"],remote_path='/home/laurent/test',preserve_times=True)
scp.close()

os.remove("text.txt")