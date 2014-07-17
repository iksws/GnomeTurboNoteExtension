from gi.repository import Gtk
import notifyturbo
from config_note import Config
from subprocess import call
import sys,os
config_note = Config()        
path_icon = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/"
path = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/"
from PyQt4.QtCore import QCoreApplication
import sys

# Ubuntu's notify-osd doesn't officially support actions. However, it does have
# a dialog fallback which we can use for this demonstration. In real use, please
# respect the capabilities the notification server reports!
OVERRIDE_NO_ACTIONS = True

class MyApp(QCoreApplication):
    def __init__(self, argv,nome,conteudo,ipsender,img_atach):
        super(MyApp, self).__init__(argv)
        # This needs to be before any other use of notifyturbo, but after the Qt
        # application has been instantiated.
        notifyturbo.init("Multi Action Test", mainloop='qt')
        
        config_note = Config()        
        path_icon = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/"
        path = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/"
        
        server_capabilities = notifyturbo.get_server_caps() 
        
        if nome.find("=") == 1:
            nome = nome[2:]
            n = notifyturbo.Notification(nome,conteudo,(path_icon + "turbo.png"))
        else:
            n = notifyturbo.Notification(nome,conteudo,(path_icon + "turbo.png"))

        #if ('actions' in server_capabilities) or OVERRIDE_NO_ACTIONS:
        data = [nome,conteudo,ipsender]
        n.add_action("resp", "Responder", self.resp_cb,data)
        n.add_action("ignore", "Ignorar", self.ignore_cb)
        if img_atach != "None":
            lista_nome = os.listdir(img_atach)
            if lista_nome[0].find("png") != -1 or lista_nome[0].find("jpg")  != -1 or lista_nome[0].find("jpeg") or  lista_nome[0].find("wmf")  != -1 or lista_nome[0].find("gif")  != -1 or lista_nome[0].find("bmp")  != -1:    
                n.add_action("images", "Image(s)", self.attaches_cb,img_atach + lista_nome[0])
            else:
                n.add_action("attached", "Attached", self.attaches_cb2,img_atach + lista_nome[0])
                
        n.set_urgency(notifyturbo.URGENCY_CRITICAL)
        n.set_category("device")
        n.show()

    def resp_cb(self,n, action,data):
        assert action == "resp"  
        try:        
            call(["python", path + "caixa.py",""+ data[0] +"","" + data[2] + "","" + data[1] + ""]) 
            #Gtk.main_quit()
            n.close()            
        except ValueError:
            print("saindo de erro....")

    def attaches_cb2(self,n, action,data):
        assert action == "attached"  
        try:        
            call(["gnome-open", data]) 
            #Gtk.main_quit()
            n.close()            
        except ValueError:
            print("saindo de erro....")

    def attaches_cb(self,n, action,data):
        assert action == "images"  
        try:        
            call(["eog", data]) 
            #Gtk.main_quit()
            n.close()            
        except ValueError:
            print("saindo de erro....")

    def ignore_cb(self,n, action):
        assert action == "ignore"
        try:
            print("Notification closed")
            #Gtk.main_quit()
            n.close()
            #notifyturbo.uninit()
        except ValueError:
            print("saindo de erro....")          


if __name__ == "__main__":
    args = sys.argv[1:]
    MyApp(sys.argv, args[0], args[1], args[2],args[3]).exec_()
