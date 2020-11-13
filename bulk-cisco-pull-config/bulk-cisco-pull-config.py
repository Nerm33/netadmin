import os
from os.path import join as pjoin
import re
import socket
import sys
import netmiko
from getpass import getpass
from datetime import date

#Set script variables
ips = []
username = input('Username: ')
password = getpass()
f_path = pjoin(os.getcwd(), 'results')

def to_doc_w(file_name, variable):
        file = pjoin(f_path, file_name)
        f = open(file, 'w')
        f.write(variable)
        f.close()	
	
def to_doc_a(file_name, varable):
	f=open(file_name, 'a')
	f.write(varable)
	f.close()

def pull_run(username,password,net_connect,ip):
	hostname = net_connect.find_prompt()[:-1]
	running_config = hostname + "_" + str(date.today()) + ".txt"
	to_doc_w(running_config, net_connect.send_command_expect('show run'))

def get_ip (input):
	return(re.findall(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', input))
	
def get_ips (file_name):
    for line in open(file_name, 'r').readlines():
        line = get_ip(line)
        for ip in line:
            ips.append(ip)

def test_dir():
    if not os.path.exists("results"):
            os.mkdir("results")

def main():
    for ip in ips:
            try:
                    print('~' * 79)
                    print('Connecting to', ip)
                    print()
                    net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
                    print('Connected to', ip)
                    pull_run(username,password,net_connect,ip)
                    print('Config file copied to', f_path)
            except socket.timeout:
                    print ('Error: Connection to device', ip, 'timed out')
            except:
                    print ('Error: Something went wrong connecting to', ip)

get_ips('ip-list.txt')

test_dir()

main()
