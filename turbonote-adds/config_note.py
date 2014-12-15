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
image_color_title_revert = False
multiThread = True #multi note or not

class Config():
	def __init__(self):
		owner = getpass.getuser()
		image_color = ""
		image_color_title_revert = False
		ip = get_ip('eth0')
		multiThread = True

	def getOwner(self):
		return owner;

	def getNotify(self):
		return multiThread;

	def getColorRevertTitle(self):
		return image_color_title_revert;

	def getColor(self):
		return image_color;

	def getColorOver(self):
		if image_color == "_b":
			return ""
		else:
			return "_b"		

	def getIp(self):
		return ip;	
