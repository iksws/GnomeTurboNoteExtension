#!/usr/bin/env python
#by ikswss@gmail.com

from gi.repository import Gtk,Gdk
import sys,os
import sqlite3
import notifyturbo
from subprocess import call
from config_note import Config

config_note = Config()
path = "/usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/"
path_icon = "/usr/share/cinnamon/applets/turbonote@iksws.com.br/icons/"

lista_hist = []
lista_histfull = []

def resp_cb(n, action,data):
    assert action == "resp"  
    try:        
        connb = sqlite3.connect(path + 'turbo.db')
        a = connb.cursor()
        a.execute("SELECT ip FROM contacts WHERE upper(nome) =  '" +  data[0] + "'" )
        try:
            ip_sender =  str(a.fetchone()[0])            
        except (RuntimeError, TypeError, NameError):
            pass
            ip_sender = ""

        connb.close()
        msgerror = "this contact does not exist!"
        print ip_sender
        if not ip_sender:
            command = "notify-send --hint=int:transient:1 \"TurboNote Gnome3\" \"" + (msgerror).decode('iso-8859-1').encode('utf8') + "\" -i " + path_icon + "turbo.png"                  
            os.system(command)        
        else:            
            call(["python", path + "caixa.py",""+ data[0] +"","" + str(ip_sender) + "","" + data[1] + ""])   
        #Gtk.main_quit()                     
    except ValueError:
        print("saindo de erro....")


def ignore_cb(n, action):
    assert action == "ignore"
    try:
        print("Notification closed")
        #Gtk.main_quit()
        n.close()
        #Gtk.main_quit()
    except ValueError:
        print("saindo de erro....")

def cap(s, l):
    return s if len(s)<=l else s[0:l-3]+'...'

connb = sqlite3.connect(path + 'turbo.db')
a = connb.cursor()
a.execute("SELECT id,nome,conteudo,data FROM history order by id desc")
rows =  a.fetchall()
for history in rows:
    lista_hist.append([str(history[0]),history[1],cap(history[2],50),history[3]])

connc = sqlite3.connect(path + 'turbo.db')
c = connc.cursor()
c.execute("SELECT id,nome,conteudo,data FROM history order by id desc")
rowsc =  c.fetchall()
for history in rowsc:
    lista_histfull.append([str(history[0]),history[1],history[2].encode("utf-8"),history[3]])

connb.close()



def rmvhistory(idnote):
    connc = sqlite3.connect(path + 'turbo.db')
    c = connc.cursor()
    c.execute("delete from history where id = '"+ (idnote) + "'")
    connc.commit()
    connc.close()

def rmvhistoryall():
    connc = sqlite3.connect(path + 'turbo.db')
    c = connc.cursor()
    c.execute("delete from history")
    connc.commit()
    connc.close()    

def treeview_clicked(widget, event,data):

    (model, iter) = data.get_selected_rows()
    iters = []
    
    for row in iter:
            iters.append(model.get_iter(row))

    if event.type == Gdk.EventType._2BUTTON_PRESS and event.button == 1:    
        server_capabilities = notifyturbo.get_server_caps()  
    
        for i in range(len(lista_histfull)):
           if lista_histfull[i][0] == model[iter][0]:               
                n = notifyturbo.Notification((model[iter][1]) ,(lista_histfull[i][2]) ,(path_icon + "turbo.png"))            

                if ('actions' in server_capabilities) or OVERRIDE_NO_ACTIONS:
                    n.add_action("resp", "Reply", resp_cb,[model[iter][1],lista_histfull[i][2]])
                    n.add_action("ignore", "Close", ignore_cb)
                    n.set_timeout(5)
                    n.show()
        return True
    

    if event.button == 1 and event.type == Gdk.EventType.BUTTON_PRESS:
         return False 

def searching(self,entry,model):
    lista_hist[:] = []
    lista_histfull[:] = []


    connb = sqlite3.connect(path + 'turbo.db')
    a = connb.cursor()    
    a.execute("SELECT id,nome,conteudo,data FROM history where conteudo like '%" + entry.get_text() + "%' order by id desc")
    rows =  a.fetchall()
    for history in rows:
        lista_hist.append([str(history[0]),history[1],cap(history[2],200),history[3]])

    connc = sqlite3.connect(path + 'turbo.db')
    c = connc.cursor()
    c.execute("SELECT id,nome,conteudo,data FROM history where conteudo like '%" + entry.get_text() + "%' order by id desc")
    rowsc =  c.fetchall()
    for history in rowsc:
        lista_histfull.append([str(history[0]),history[1],history[2].encode("utf-8"),history[3]])

    connb.close()

    if len(model) != 0:
        for i in range(len(model)):
            iter = model.get_iter(0)
            model.remove(iter)                

    for i in range(len(lista_hist)):
        model.append(lista_hist[i])



class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="History Received Note List")
        self.set_default_size(1000, 500)            
        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "History Received Note List"

        box2 = Gtk.VBox(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box2.get_style_context(), "linked")

        self.set_titlebar(hb)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_from_file("/usr/share/cinnamon/applets/turbonote@iksws.com.br/icons/turbo.png")
        self.set_wmclass ("TurboNote Gnome", "TurboNote Gnome")
        grid = Gtk.Grid()
        self.set_border_width(15)
        scroller = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        scroller.set_shadow_type(2)
        scroller.set_border_width(border_width=1)
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.searchtxt = Gtk.SearchEntry() 
        self.label3 = Gtk.Label()
        self.label3.set_text(" ") 
        self.searchtxt.set_tooltip_text("[press Enter to search]")
        grid.attach(self.searchtxt, 0, 1, 3, 1)        
        grid.attach(self.label3, 0, 3, 3, 1) 
        grid.attach(scroller, 0, 4, 3, 1)     
         
        treeview = Gtk.TreeView()
        treeview.set_enable_tree_lines(True)
        treeview.set_grid_lines(1)
        treeview.set_tooltip_text("[Double click to view note again]")

        cell  = Gtk.CellRendererText(weight=300)
        cell2 = Gtk.CellRendererText(weight=300)
        cell3 = Gtk.CellRendererText(weight=300)
        cell4 = Gtk.CellRendererText(weight=300)

        cell.set_fixed_size(50, 5)
        cell2.set_fixed_size(200, -1)
        cell3.set_fixed_size(500, -1)
        cell4.set_fixed_size(150, -1)

        col  = Gtk.TreeViewColumn("ID",    cell, text=0)
        col2 = Gtk.TreeViewColumn("Name", cell2, text=1)
        col3 = Gtk.TreeViewColumn("Data", cell3, text=2)
        col4 = Gtk.TreeViewColumn("Date", cell4, text=3)

        treeview.append_column(col)
        treeview.append_column(col2)
        treeview.append_column(col3)
        treeview.append_column(col4)

        cell.set_visible(False)
        col.set_visible(False)

        col2.set_sort_column_id(0)
        col3.set_sort_column_id(0)
        col4.set_sort_column_id(0)

        scroller.add(treeview)
 
        self.model = Gtk.ListStore(str,str,str,str)             
        treeview.set_model(self.model)
        
        for i in range(len(lista_hist)):
            self.model.append(lista_hist[i])
 
        self.searchtxt.connect("activate", searching, self.searchtxt,self.model) 

        self.selection = treeview.get_selection()
        treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        treeview.connect("button-press-event", treeview_clicked,self.selection) 

        self.label = Gtk.Label()
        self.label.set_text(" ")

        self.button_remove = Gtk.Button()
        self.button_remove.connect("clicked", self.remove_cb)
        self.button_remove_all = Gtk.Button()
        self.button_remove_all.connect("clicked", self.remove_all_cb)

        self.removeimg = Gtk.Image()  
        if config_note.getColorRevertTitle():
            self.removeimg.set_from_file("/usr/share/cinnamon/applets/turbonote@iksws.com.br/icons/ic_action_storage" + config_note.getColorOver() + ".png")      
        else:
            self.removeimg.set_from_file("/usr/share/cinnamon/applets/turbonote@iksws.com.br/icons/ic_action_storage" + config_note.getColor() + ".png")      
        self.button_remove.add(self.removeimg)  

        self.removeallimg = Gtk.Image()  
        if config_note.getColorRevertTitle():
            self.removeallimg.set_from_file("/usr/share/cinnamon/applets/turbonote@iksws.com.br/icons/ic_action_storage_all" + config_note.getColorOver() + ".png")        
        else:               
            self.removeallimg.set_from_file("/usr/share/cinnamon/applets/turbonote@iksws.com.br/icons/ic_action_storage_all" + config_note.getColor() + ".png")        
        self.button_remove_all.add(self.removeallimg)

        
        
       
        self.add(grid)   
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")           
        
        box.add(self.button_remove)
        box.add(self.button_remove_all)
        hb.pack_start(box)

        self.button_remove.set_tooltip_text("Remove selected")
        self.button_remove_all.set_tooltip_text("Remove all")
        
        notifyturbo.init("TurboNote Gnome 3", mainloop="glib")
        
    def remove_cb(self, button):
        if len(self.model) != 0:
            (self.model, iter) = self.selection.get_selected_rows()
            iters = []

            for row in iter:                
                iters.append(self.model.get_iter(row))              
                
            if len(iters) != 0:
                for i in range(len(iters)):                                     
                    rmvhistory(self.model[iters[i]][0])
                    self.model.remove(iters[i])   
            else:
                msgerror = "No select Note!\\nPlease select one Note to remove!";                      
                command = "notify-send --hint=int:transient:1 \"TurboNote Gnome3\" \"" + (msgerror).decode('iso-8859-1').encode('utf8') + "\" -i " + path_icon + "turbo.png"                  
                os.system(command)        
        else:
            msgerror = "Empty list!\\nYou don't have Notes to remove!";                      
            command = "notify-send --hint=int:transient:1 \"TurboNote Gnome3\" \"" + (msgerror).decode('iso-8859-1').encode('utf8') + "\" -i " + path_icon + "turbo.png"                  
            os.system(command)        

    def remove_all_cb(self, button):
        if len(self.model) != 0:
            for i in range(len(self.model)):
                iter = self.model.get_iter(0)
                self.model.remove(iter)
                rmvhistoryall()

        msgerror = "Empty list!\\nAll Notes removed!";                      
        command = "notify-send --hint=int:transient:1 \"TurboNote Gnome3\" \"" + (msgerror).decode('iso-8859-1').encode('utf8') + "\" -i " + path_icon + "turbo.png"                  
        os.system(command)        


if __name__ == "__main__":
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
