#!/usr/bin/env python
#by ikswss@gmail.com

import socket, struct, fcntl
import getpass

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd = sock.fileno()
SIOCGIFADDR = 0x8915
owner = getpass.getuser()

def get_ip(iface = 'eth0'):
	ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)
	try:
		res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
	except:
		return None
	
	ip = struct.unpack('16sH2x4s8x', res)[2]
	return socket.inet_ntoa(ip)

ip = get_ip('eth0')
image_color = "" # _b for black

class Config():
	 def __init__(self):
		owner = getpass.getuser()
		image_color = ""
		ip = get_ip('eth0')

		print "YOUR CONFS"
		print "IP: " + ip
		print "USERNAME: " + owner.upper()

		if self.getColor() == "":
			print "COLOR ICONS: WHITE"
		else:
			print "COLOR ICONS: BLACK"


	 def getOwner(self):
	 		return owner;
	 def getColor(self):
	 		return image_color;

	 def getIp(self):
	 		return ip;	