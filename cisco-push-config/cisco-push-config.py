import os
from os.path import join as pjoin
import re
import socket
import sys
import netmiko
from getpass import getpass


# Define script functions
def to_doc_w(file_name, variable):
    file_path = pjoin(os.getcwd(), "results")
    file = pjoin(file_path, file_name)
    f = open(file, 'w')
    f.write(variable)
    f.close()


def to_doc_a(file_name, variable):
    f = open(file_name, 'a')
    f.write(variable)
    f.close()


def pull_run(username, password, net_connect, ip):
    hostname = net_connect.find_prompt()[:-1]
    running_config = hostname + "running_config.txt"
    to_doc_w(running_config, net_connect.send_command_expect(commands))


def get_ip(input):
    return (
        re.findall(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', input))


def get_ips(file_name):
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
            print('Connecting to device:', ip)
            print()
            net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
            pull_run(username, password, net_connect, ip)
            print(net_connect.send_command_expect(commands))
        except socket.timeout:
            print("Failed connecting to device:", ip)


# Set script variables
ips = []
get_ips("ip-list.txt")
username = input("Username: ")
password = getpass()

# Set commands variable from file
with open('cisco-commands.txt') as f:
    lines = f.read().splitlines()
print(lines)
commands = "\n".join(lines)

# Run test_dir function
test_dir()

# Run main script function
main()
