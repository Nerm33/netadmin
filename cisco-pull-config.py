import os
import re
import socket
import sys
import netmiko
from getpass import getpass

username = input("Username: ")
password = getpass() 
ip = input("Device IP: ")


def to_doc_w(file_name, varable):
	f=open(file_name, 'w')
	f.write(varable)
	f.close()	

def pull_run(username,password,net_connect,ip):
	hostname = net_connect.find_prompt()[:-1]
	running_config = hostname + " running_config.txt"
	to_doc_w(running_config, net_connect.send_command_expect('show run'))

def main():
	try:
		net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
		pull_run(username,password,net_connect,ip)
	except socket.timeout:
			print ("Failed connecting to device:", ip)

main()
