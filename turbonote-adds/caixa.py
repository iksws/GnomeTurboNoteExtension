#!/usr/bin/env python
#by ikswss@gmail.com
from gi.repository import Gtk,Gdk
import re
import time
import cStringIO
import sys
from subprocess import call
import threading
from config_note import Config
from list_control import MyWindow

#call config class for get parameters
config_note = Config()
path = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/"

#defini variables
attpick = True
attFile = ""
stay = ""

#get and setters
def assignNewValueToStay(s):
    global stay
    stay = s

def assignNewValueToAttFile(f):
    global attFile
    attFile = f

def assignNewValueToAttPick(p):
    global attpick
    attpick = p

#python Gtk class window
class TextViewWindow(Gtk.Window):
	def __init__(self,titulo,ip,msg_rec,nome):
		#layout config
		Gtk.Window.__init__(self, title = "To " + titulo)
		self.set_default_size(300, 300)
		self.set_border_width(15)     
		self.set_position(Gtk.WindowPosition.CENTER)
		self.grid = Gtk.Grid()
		self.add(self.grid)
		self.create_textview() 	
		self.set_icon_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/turbo.png")    
		self.set_wmclass ("TurboNote Gnome", "TurboNote Gnome")
		self.connect('key-press-event',on_button_clicked2,nome)


	def create_textview(self):
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)		
		scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		self.grid.attach(scrolledwindow, 0, 1, 4, 1)

		self.textview = Gtk.TextView()
		self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
		self.textview.set_border_width(border_width=10)
		self.textbuffer = self.textview.get_buffer()

		msglinux = msg_rec.replace("\\n","#")
		
		msgsplitlinux = msglinux.split('#')
		msg_unicode = ""

		for i in range(len(msgsplitlinux)):                           
			msg_unicode = msg_unicode+ (msgsplitlinux[i].replace("\\r"," ") + "\n")

		self.textbuffer.set_text(msg_unicode)
		scrolledwindow.add(self.textview) 

		self.attachedbt = Gtk.Button()
		self.attachedbtrmv = Gtk.Button() 

		self.label = Gtk.Label()
		self.label.set_text(" ")

		self.label3 = Gtk.Label()
		self.label3.set_text(" ") 

		self.labelattached = Gtk.Label()
		self.labelattached.set_text("") 


		self.toggle_stay = Gtk.ToggleButton()
		self.toggle_stay.connect("toggled", self.toggle_stay_callback)	

		responderbt = Gtk.Button()
		
		responderbt.connect("clicked", self.on_button_clicked,nome)

		sendcontact = Gtk.Button()
		sendcontact.connect("clicked", self.on_button_contact)

		self.staytop = Gtk.Image()	
		self.staytop.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_action_cast" + config_note.getColor() + ".png")		
		self.toggle_stay.add(self.staytop)	

		self.sending = Gtk.Image()	
		self.sending.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_action_send_now" + config_note.getColor() + ".png")		
		sendcontact.add(self.sending)
	
		self.replyico = Gtk.Image()	
		self.replyico.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_action_repley_now" + config_note.getColor() + ".png")		
		responderbt.add(self.replyico)

		self.addattimg = Gtk.Image()	
		self.addattimg.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_action_new_attachment" + config_note.getColor() + ".png")		
		self.attachedbt.add(self.addattimg)

		self.addattimgrmv = Gtk.Image()	
		self.addattimgrmv.set_from_file("/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/ic_remove_attached" + config_note.getColor() + ".png")		
		self.attachedbtrmv.add(self.addattimgrmv)	

		self.attachedbt.connect("clicked", self.on_file_clicked)		
		self.attachedbtrmv.connect("clicked", self.on_file_clicked_rmv)	

		self.grid.attach(self.label, 0, 2, 4, 1)

		self.grid.attach(self.toggle_stay, 0, 5, 1, 1)
		self.grid.attach(responderbt, 1, 5, 1, 1)	
		self.grid.attach(sendcontact, 2, 5, 1, 1)
		self.grid.attach(self.attachedbt, 3, 5, 1, 1)
		self.grid.attach(self.attachedbtrmv, 3, 5, 1, 1)

	def on_file_clicked_rmv(self, widget):
		self.labelattached.set_text("")
		assignNewValueToAttFile("")
		self.attachedbt.show()	
		self.attachedbtrmv.hide()	
		self.label3.hide()
		self.labelattached.hide()	

	def on_file_clicked(self, widget):
		if attpick:
			self.grid.attach(self.label3, 0, 4, 4, 1)			
			self.grid.attach(self.labelattached, 0, 3, 4, 1)
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


	def toggle_stay_callback(self, button):
	    if self.toggle_stay.get_active():
	        assignNewValueToStay("Yes")
	    else:
	        assignNewValueToStay("")	

	def on_button_clicked(self, widget,nome):
		buf  = self.textview.get_buffer()
		text = buf.get_text(buf.get_start_iter(),buf.get_end_iter(),True)
		#win = MyWindow(text.decode('utf-8').encode('windows-1252'))
		#win.connect("delete-event", Gtk.main_quit)
		#win.show_all()
		#Gtk.main()
		s = threading.Thread(target=send_turbo ,args=(text,ip,nome))
		s.start()
		Gtk.main_quit() 

	def on_button_contact(self,button):
		print "aki"
		buf  = self.textview.get_buffer()
		text = buf.get_text(buf.get_start_iter(),buf.get_end_iter(),True)
		win = MyWindow(text.decode('utf-8').encode('windows-1252'),stay,attFile)
		win.connect("delete-event", Gtk.main_quit)
		win.show_all()
		Gtk.main()
		#s = threading.Thread(target=send_turbo_contact ,args=(text,ip))
		#s.start()
		#Gtk.main_quit() 

	
def on_button_clicked2(self, event,nome):
	keyval = event.keyval
	name = Gdk.keyval_name(keyval)
	mod = Gtk.accelerator_get_label(keyval,event.state)
	if mod == "Ctrl+Mod2+Return" or mod == "Ctrl+Mod2+Enter":
		buf  = self.textview.get_buffer()
		text = buf.get_text(buf.get_start_iter(),buf.get_end_iter(),True)
		win = MyWindow(text.decode('utf-8').encode('windows-1252'),stay,attFile)
		win.connect("delete-event", Gtk.main_quit)
		win.show_all()
		Gtk.main()
	if mod == "Ctrl+Mod2+R":
		buf  = self.textview.get_buffer()
		text = buf.get_text(buf.get_start_iter(),buf.get_end_iter(),True)
		s = threading.Thread(target=send_turbo ,args=(text,ip,nome))
		s.start()
		Gtk.main_quit() 

#def send_turbo_contact(message,ip):
	#win = MyWindow(message.decode('utf-8').encode('windows-1252'))
	#win.connect("delete-event", Gtk.main_quit)
	#win.show_all()
	#Gtk.main()
	#call(["python", path + "list_control.py",""+ message.decode('utf-8').encode('windows-1252') + ""])
	#Gtk.main_quit()

def send_turbo(message,ip,nome):  
	call(["python", path + "cliente.py",""+ message.decode('utf-8').encode('windows-1252') + "","" + ip + "","" + nome + "","" + stay + "","" + "" + "", "" + attFile + ""])        


if __name__ == "__main__":
	args = sys.argv[1:]
	ip = args[1]
	nome = args[:1]
	nome = str(nome)[:-2][2:]

	#msg_rec = args[2:]
	#msg_rec = (msg_rec)[:-2][2:]
	nome = nome.decode('iso-8859-1').encode('utf8')
	
	msg_rec = args[2]

	win = TextViewWindow(nome,ip,msg_rec,nome)
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()
