#!/usr/bin/env python
#by ikswss@gmail.com

from gi.repository import Gtk,Gdk
import re
import time
import cStringIO
import sys,os
from subprocess import call
import threading
from config_note import Config

config_note = Config()
path = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/"
pathIcon = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/"

class HeaderBarWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title = "About TurboNote Gnome3")
		self.set_default_size(100, 380)
		self.set_border_width(15)  
		hb = Gtk.HeaderBar()
		hb.props.show_close_button = True
		hb.props.title = "About TurboNote Gnome3"
		box2 = Gtk.VBox(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(box2.get_style_context(), "linked")
		self.set_titlebar(hb)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.grid = Gtk.Grid()
		self.add(self.grid)
		self.create_textview()
		self.set_icon_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/turbo.png")
		self.set_wmclass ("TurboNote Gnome", "TurboNote Gnome")
		self.connect('key-press-event',on_button_clicked2)

	def create_textview(self):
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		self.grid.attach(scrolledwindow, 0, 1, 4, 1)	

		self.label = Gtk.Label()
		self.label.set_text("Thank you for using this extension, reporting bugs in  \nhttps://github.com/iksws/GnomeTurboNoteExtension\n\nDeveloper mail: ikswss@gmail.com\n\n") 
		scrolledwindow.add(self.label) 

		responderbt = Gtk.Button("       Close       ")		
		donatebt = Gtk.Button("Make a Donate! :)")		

		box = Gtk.VBox(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(box.get_style_context(), "linked")
		
		box.add(donatebt)
		box.add(responderbt)

		scrolledwindow2 = Gtk.ScrolledWindow()
		scrolledwindow2.set_hexpand(True)
		scrolledwindow2.set_vexpand(True)
		scrolledwindow2.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

		
		box.set_hexpand(True)
		self.grid.attach(box, 0, 3, 1, 1)
		responderbt.connect("clicked", self.on_button_clicked)
		donatebt.connect("clicked", self.on_button_clickedDonate)

	def on_button_clicked(self, widget):		
		Gtk.main_quit() 

	def on_button_clickedDonate(self, widget):		
		os.system("firefox -new-tab https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick'&'hosted_button_id=ZVJ95XE3FKM3E");

    


	

def on_button_clicked2(self, event):
	keyval = event.keyval
	name = Gdk.keyval_name(keyval)
	mod = Gtk.accelerator_get_label(keyval,event.state)
	if mod == "Ctrl+Mod2+Return":
		buf  = self.textview.get_buffer()
		text = buf.get_text(buf.get_start_iter(),buf.get_end_iter(),True)
		send_turbo(text.decode('utf-8').encode('windows-1252'))
		Gtk.main_quit() 

def send_turbo(message):
	call(["python", path + "list_control.py",""+ message + ""])
	Gtk.main_quit()


win = HeaderBarWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
