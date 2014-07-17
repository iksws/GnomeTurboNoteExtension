#!/usr/bin/env python
from gi.repository import Gtk,Gdk
import re
import time
import cStringIO
import sys,os
from subprocess import call
import threading
from config_note import Config
from list_control import MyWindow

config_note = Config()
path = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/"
pathIcon = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/"
stay = ""

def assignNewValueToStay(s):
    global stay
    stay = s

onepick = True

def assignNewValueToOnePick(p):
    global onepick
    onepick = p

attpick = True

attFile = ""

def assignNewValueToAttFile(f):
    global attFile
    attFile = f

def assignNewValueToAttPick(p):
    global attpick
    attpick = p


class TextViewWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title = "New Note")
		self.set_icon_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/turbo.png")	
		self.set_default_size(300, 300)
		self.set_border_width(15)     
		self.set_position(Gtk.WindowPosition.CENTER)
		self.grid = Gtk.Grid()
		self.add(self.grid)
		self.create_textview()    
		self.set_wmclass ("TurboNote Gnome", "TurboNote Gnome")
		self.connect('key-press-event',on_button_clicked2)


	def create_textview(self):
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		self.grid.attach(scrolledwindow, 0, 3, 5, 1)

		self.textview = Gtk.TextView()
		self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
		self.textview.set_border_width(border_width=10)
		self.textbuffer = self.textview.get_buffer()
		self.textbuffer.set_text("")
		scrolledwindow.add(self.textview) 

		self.label = Gtk.Label()
		self.label.set_text(" ") 
		self.label2 = Gtk.Label()
		self.label2.set_text(" ") 
		self.label3 = Gtk.Label()
		self.label3.set_text(" ") 

		self.labelattached = Gtk.Label()
		self.labelattached.set_text("") 

		self.toggle_stay = Gtk.ToggleButton()
		self.toggle_stay.connect("toggled", self.toggle_stay_callback)

		self.toggle_titulo = Gtk.ToggleButton()
		self.toggle_titulo.connect("toggled", self.toggle_titulo_callback)

		self.titulotxt = Gtk.Entry()
		responderbt = Gtk.Button()		
		scshot = Gtk.Button()	
		self.attachedbt = Gtk.Button()
		self.attachedbtrmv = Gtk.Button()

		self.attachedbt.connect("clicked", self.on_file_clicked)		
		self.attachedbtrmv.connect("clicked", self.on_file_clicked_rmv)		
		
		self.photo = Gtk.Image()	
		self.photo.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_action_camera" + config_note.getColor() + ".png")		
		scshot.add(self.photo)

		self.sending = Gtk.Image()	
		self.sending.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_action_send_now" + config_note.getColor() + ".png")		
		responderbt.add(self.sending)

		self.staytop = Gtk.Image()	
		self.staytop.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_action_cast" + config_note.getColor() + ".png")		
		self.toggle_stay.add(self.staytop)	

		self.enabletitle = Gtk.Image()	
		self.enabletitle.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_action_labels" + config_note.getColor() + ".png")		
		self.toggle_titulo.add(self.enabletitle)

		self.addattimg = Gtk.Image()	
		self.addattimg.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_action_new_attachment" + config_note.getColor() + ".png")		
		self.attachedbt.add(self.addattimg)

		self.addattimgrmv = Gtk.Image()	
		self.addattimgrmv.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_remove_attached" + config_note.getColor() + ".png")		
		self.attachedbtrmv.add(self.addattimgrmv)	
	

		self.grid.attach(self.label, 0, 4, 5, 1)	
		self.grid.attach(self.toggle_stay, 0, 7, 1, 1)
		self.grid.attach(self.toggle_titulo, 1, 7, 1, 1)	
		self.grid.attach(scshot, 2 , 7, 1, 1)	
		self.grid.attach(responderbt, 3, 7, 1, 1)
		self.grid.attach(self.attachedbt, 4, 7, 1, 1)
		self.grid.attach(self.attachedbtrmv, 4, 7, 1, 1)
		
	

		responderbt.connect("clicked", self.on_button_clicked)
		scshot.connect("clicked", self.on_button_ss)

	def on_file_clicked_rmv(self, widget):
		self.labelattached.set_text("")
		assignNewValueToAttFile("")
		self.attachedbt.show()	
		self.attachedbtrmv.hide()	
		self.label3.hide()
		self.labelattached.hide()	

	def on_file_clicked(self, widget):
		if attpick:
			self.grid.attach(self.label3, 0, 6, 5, 1)			
			self.grid.attach(self.labelattached, 0, 5, 5, 1)
			self.attachedbtrmv.hide()				
			assignNewValueToAttPick(False)			
		dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
  		  		
  		resp = dialog.run()

  		if resp == Gtk.ResponseType.OK:     
	  		self.label3.show()
			self.labelattached.show()			
			filename = dialog.get_filename()
			filename = filename.split("/")
			assignNewValueToAttFile(dialog.get_filename())
			self.labelattached.set_markup("Attached file <b>" + filename[len(filename)-1] +  "</b>") 
			self.attachedbt.hide()
			self.attachedbtrmv.show()			

		elif resp == Gtk.ResponseType.CANCEL:
			self.labelattached.set_text("") 
			assignNewValueToAttFile("")

		dialog.destroy()

	def on_button_clicked(self, widget):
		buf  = self.textview.get_buffer()
		text = buf.get_text(buf.get_start_iter(),buf.get_end_iter(),True)
		send_turbo(text.decode('utf-8').encode('windows-1252'),self.titulotxt.get_text(),attFile)
		#Gtk.main_quit() 

	def on_button_ss(self, widget):
		os.system("gnome-screenshot -i -a") 		
		#Gtk.main_quit() 

	def toggle_stay_callback(self, button):
	    if self.toggle_stay.get_active():
	        assignNewValueToStay("Yes")
	    else:
	        assignNewValueToStay("")

	def toggle_titulo_callback(self, button):
	    if self.toggle_titulo.get_active():
	    	if onepick:
	    		self.grid.attach(self.label2, 0, 2, 5, 1)
	    		self.grid.attach(self.titulotxt, 0, 1, 5, 1)	 
	    		assignNewValueToOnePick(False)   	
	        self.titulotxt.show()
	        self.label2.show()
	    else:
	    	self.titulotxt.set_text("")
	        self.titulotxt.hide()
	        self.label2.hide()

def on_button_clicked2(self, event):
	keyval = event.keyval
	name = Gdk.keyval_name(keyval)
	mod = Gtk.accelerator_get_label(keyval,event.state)
	if mod == "Ctrl+Mod2+Return" or mod == "Ctrl+Mod2+Enter":
		buf  = self.textview.get_buffer()
		text = buf.get_text(buf.get_start_iter(),buf.get_end_iter(),True)
		send_turbo(text.decode('utf-8').encode('windows-1252'),self.titulotxt.get_text(),attFile)
		#Gtk.main_quit() 

def send_turbo(message,titulo,att):
	win = MyWindow(message,stay,att,titulo)
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()
	#call(["python", path + "list_control.py",""+ message + ""])
	#Gtk.main_quit()


if __name__ == "__main__":
	win = TextViewWindow()
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()
