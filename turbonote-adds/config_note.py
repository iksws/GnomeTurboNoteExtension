#!/usr/bin/env python
#by ikswss@gmail.com

import socket, struct, fcntl
import getpass

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd = sock.fileno()
SIOCGIFADDR = 0x8915
owner = getpass.getuser()

def get_ip(iface = 'eth0'):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("google.com",80))
	ip =  (s.getsockname()[0])
	s.close()
	return ip	

ip = get_ip('eth0')
image_color = "_b" # _b for black

class Config():
	def __init__(self):
		owner = getpass.getuser()
		image_color = ""
		ip = get_ip('eth0')

	def getOwner(self):
		return owner;
	def getColor(self):
		return image_color;

	def getIp(self):
		return ip;	
