#!/usr/bin/env python
#by ikswss@gmail.com

from gi.repository import Gtk, Gdk,GObject
import commands
import time
import sys,os
import os.path
import threading
path = "/usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/"
path_icon = "/usr/share/cinnamon/applets/turbonote@iksws.com.br/icons/"

class ProgressBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="SVN UPDATE")
        self.set_default_size(800, 400)
        self.set_border_width(15)      
        self.set_position(Gtk.WindowPosition.CENTER)
        
        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "SVN UPDATE"        
        self.set_titlebar(hb)    

        self.progressbar = Gtk.ProgressBar()

        self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)

        self.progressbar.set_text("Checking for updates in SVN")
        self.progressbar.set_show_text("Checking for updates in SVN")        
      
        self.grid = Gtk.Grid()
        self.add(self.grid)        
        self.textview = Gtk.TextView()

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_shadow_type(2)
        scrolledwindow.set_border_width(border_width=1)
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolledwindow.add_with_viewport(self.textview )
        
        scrolledwindow.connect("size-allocate", self._autoscroll)
        self.textview.set_property('editable', False)

        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textview.set_border_width(10)
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("")
        scrolledwindow.add(self.textview) 

        self.titulotxt = Gtk.Entry()
        self.label2 = Gtk.Label()
        self.label2.set_text("\nNeed root password:\n") 

        self.send = Gtk.Button("OK")              

        self.grid.attach(self.progressbar, 0, 0, 1 , 1)
        self.label = Gtk.Label()
        self.label.set_text(" ")         
        self.grid.attach(self.label, 0, 1, 1 , 1)
        self.grid.attach(scrolledwindow, 0, 2, 1 , 1)

        self.grid.attach(self.label2, 0, 3, 1 , 1)
        self.grid.attach(self.titulotxt, 0, 4, 1 , 1)
        self.grid.attach(self.send, 0, 5, 1 , 1)

        buffer = self.textview.get_buffer()                       
        self.send.connect("clicked", self.checkpw,buffer) 

        bg_color = Gdk.RGBA()
        bg_color.parse("#000000")

        tx_color = Gdk.RGBA()
        tx_color.parse("#FFFFFF")

        self.textview.override_color(Gtk.StateType.NORMAL, tx_color)
        self.textview.override_background_color(Gtk.StateType.NORMAL, bg_color)
        self.progressbar.hide()
        self.titulotxt.set_visibility(False)

    def checkpw(self,widget,buffer):
        if self.titulotxt.get_text() != "":
            self.titulotxt.hide()
            self.label2.hide()
            self.send.hide()
            self.update_now(buffer)
        else:
            msgerror = "Enter root password!"
            command = "notify-send --hint=int:transient:1 \"TurboNote Gnome3\" \"" + (msgerror).decode('iso-8859-1').encode('utf8') + "\" -i " + path_icon + "turbo.png"
            os.system(command)
        

    def update_now(self,buffer):
        self.activity_mode = True     
        self.progressbar.pulse()
        t = threading.Thread(target=update,args=[buffer,self.progressbar,self,self.label,self.titulotxt.get_text()])
        t.start()

    def _autoscroll(self,scrolledwindow,*args):
            """The actual scrolling method"""
            adj = scrolledwindow.get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        if self.activity_mode:
            self.progressbar.pulse()
        else:
            new_value = self.progressbar.get_fraction() + 0.01

            if new_value > 1:
                new_value = 0

            self.progressbar.set_fraction(new_value)

        # As this is a timeout function, return True so that it
        # continues to get called
        return True

def update(buffer,progressbar,window,label,password):
    buffer.insert(buffer.get_end_iter(), str("Waiting...\n"))
    buffer.insert(buffer.get_end_iter(), str("Connecting to https://github.com/iksws/GnomeTurboNoteExtension/branches/Cinnamon...\n"))
    restart = False;
    for line in  commands.getstatusoutput('cd /usr/share/cinnamon/applets/turbonote@iksws.com.br; svn update'):
        if str(line) != '0':
            if "server.py" in line or  "applet.js" in line:
                restart = True
            buffer.insert(buffer.get_end_iter(), str(line))

    if os.path.exists("/usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/updatebd.sql"):
        statinfo = os.stat("/usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/updatebd.sql")
        if statinfo.st_size > 1:
            buffer.insert(buffer.get_end_iter(), str("\n"))
            buffer.insert(buffer.get_end_iter(), str("\nDATABASE UPDATE FOUND!"))
            buffer.insert(buffer.get_end_iter(), str("\nUPDATING DATABSE...\n"))
            os.system("sqlite3 /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/turbo.db < /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/updatebd.sql")
            os.system("echo "" > /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/updatebd.sql")

    if restart:
        buffer.insert(buffer.get_end_iter(), str("\n\nREQUIRE RESTART PRESS [ALT+F2] ENTER [r] IN INPUT BOX PRESS [ENTER]"))   

    buffer.insert(buffer.get_end_iter(), str("\n\n"))
    buffer.insert(buffer.get_end_iter(), str("Last 5 updates..."))
    buffer.insert(buffer.get_end_iter(), str("\n"))

    for line2 in  commands.getstatusoutput('svn log  https://github.com/iksws/GnomeTurboNoteExtension/trunk -l5'):
        if str(line2) != '0':
            buffer.insert(buffer.get_end_iter(), str(line2))
    
    if os.path.exists("/usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote"):
        os.system(" echo '"+ password + "' | sudo -S mv /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote /etc/init.d/")          
        buffer.insert(buffer.get_end_iter(), str("\n\nADD TURBO NOTE SERVICE!"))    

    buffer.insert(buffer.get_end_iter(), str("\n\nFINISH!"))

    progressbar.hide()  
    label.hide();
    


win = ProgressBarWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
