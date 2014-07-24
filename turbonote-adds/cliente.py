#!/usr/bin/env python

import socket
import re
import time
import cStringIO
import sys,os
from config_note import Config
from subprocess import call
from config_note import Config
import base64
import binascii
from picture import Image
from base import RawCode
import sqlite3
from datetime import datetime

config_note = Config()
path = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/"
path_icon = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/"
path_tmp = "/home/" + config_note.getOwner() + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/tmp_send/"
def client(message,ip,nome,stay,titulo="",att=""):     
      #check if have img
      files = ""
      lista_dir = os.listdir(path_tmp)
      imageBase64 = ""
      if len(lista_dir) != 0:
            files = (lista_dir[0])                  
            command1 = "mv '" + path_tmp + files + "' " + path_tmp + "fullscreen.png"            
            command2 = "cd " + path_tmp + "; zip fullscreen.zip fullscreen.rtf"
            command3 = "cd " + path_tmp + "; mv fullscreen.zip fullscreen.txt"
            os.system(command1)
            time.sleep(1)
            richTextMaker(path_tmp + "fullscreen.png")
            time.sleep(2)
            os.system(command2)            
            time.sleep(2)
            os.system(command3)

            f2 = open(path_tmp + "fullscreen.txt", 'r')
            data = f2.read()
            f2.close()
            imageBase64 = base64.b64encode(data)      

      #check if have attached
      filest = ""
      bytesattached = ""

      output = cStringIO.StringIO()
      dataAttached = cStringIO.StringIO()
      if att != "":   
            bytesattached = os.path.getsize(att)
            #f2 = open(att, 'r')
            #dataAttached = f2.read()
            #dataAttached = f2.readlines(1024)
            fh = open(att, 'rt')            
            dataAttached.write(fh.read())
            fh.close()
            #f2.close()
            filename = att.split("/")
            output.write("ATTACHED\\" + filename[len(filename)-1] + "\r\n")


      sussecs = "1"             
      ip_sender = ip.split(',')  


      for x in range(len(ip_sender)):            
            msgsplitlinux  = message.splitlines()            

            for i in range(len(msgsplitlinux)):     
                    if not msgsplitlinux[i]:
                        output.write("\r\n")
                    else:
                        output.write(msgsplitlinux[i] + "\r\n")          

            output.write("\r\n" + "End of TCPIP text#" + "\r\n")
            output.write("\r\n" + "From=" + config_note.getOwner()  + "#" + "\r\n")
            output.write("\r\n" + "SentBy=" + config_note.getOwner()  + "#" + "\r\n")
            if stay == "Yes":
                  output.write("\r\n" + "StayOnTop=Yes#" + "\r\n" )
            else:
                  output.write("\r\n" + "StayOnTop=#" + "\r\n" )
            output.write("\r\n" + "HasBorder=#" + "\r\n")
            output.write("\r\n" + "BkColor=16777215#" + "\r\n") #cores
            output.write("\r\n" + "FoColor=0#" + "\r\n") #cores
            output.write("\r\n" + "TiBkColor=0#" + "\r\n") #cores
            output.write("\r\n" + "TiFoColor=16777215#" + "\r\n") #cores
            output.write("\r\n" + "X=804#" + "\r\n")
            output.write("\r\n" + "Y=194#" + "\r\n")
            output.write("\r\n" + "Width=281#" + "\r\n")
            output.write("\r\n" + "Height=111#" + "\r\n")
            output.write("\r\n" + "Sponsored=#" + "\r\n")
            output.write("\r\n" + "LFHEIGHT=-13#" + "\r\n")
            output.write("\r\n" + "LFWIDTH=0#" + "\r\n")
            output.write("\r\n" + "LFESCAPEME=0#" + "\r\n")
            output.write("\r\n" + "LFORIENTAT=0#" + "\r\n")
            output.write("\r\n" + "LFWEIGHT=700#" + "\r\n")
            output.write("\r\n" + "LFITALIC=0#" + "\r\n")
            output.write("\r\n" + "LFUNDERLIN=0#" + "\r\n")
            output.write("\r\n" + "LFSTRIKEOU=0#" + "\r\n")
            output.write("\r\n" + "LFCHARSET=0#" + "\r\n")
            output.write("\r\n" + "LFOUTPRECI=3#" + "\r\n")
            output.write("\r\n" + "LFCLIPPREC=2#" + "\r\n")
            output.write("\r\n" + "LFQUALITY=1#" + "\r\n")
            output.write("\r\n" + "LFPITCHAND=18#" + "\r\n")
            output.write("\r\n" + "LFFACENAME=Verdana#" + "\r\n")
            output.write("\r\n" + "LFHEIGHTTI=-15#" + "\r\n")
            output.write("\r\n" + "LFWIDTHTI=0#" + "\r\n")
            output.write("\r\n" + "LFESCAPETI=0#" + "\r\n")
            output.write("\r\n" + "LFORIENTTI=0#" + "\r\n")
            output.write("\r\n" + "LFWEIGHTTI=700#" + "\r\n")
            output.write("\r\n" + "LFITALICTI=0#" + "\r\n")
            output.write("\r\n" + "LFUNDERLTI=0#" + "\r\n")
            output.write("\r\n" + "LFSTRIKETI=0#" + "\r\n")
            output.write("\r\n" + "LFCHARSETI=0#" + "\r\n")
            output.write("\r\n" + "LFOUTPRETI=3#" + "\r\n")
            output.write("\r\n" + "LFCLIPPRTI=2#" + "\r\n")
            output.write("\r\n" + "LFQUALITTI=1#" + "\r\n")
            output.write("\r\n" + "LFPITCHTI=18#" + "\r\n")
            output.write("\r\n" + "LFFACENATI=Verdana#" + "\r\n") #font
            if titulo:
                  output.write("\r\n" + "SZTITLE=" + titulo + "#" + "\r\n")
            else:
                  output.write("\r\n" + "SZTITLE=#" + "\r\n")
            if att == "":
                  output.write("\r\n" + "SZATTACHEDFILE=#" + "\r\n")
            else:
                  filename = att.split("/")
                  output.write("\r\n" + "SZATTACHEDFILE=" + filename[len(filename)-1]+ "#" + "\r\n") 
            output.write("\r\n" + "ALARMTIME=#" + "\r\n")
            output.write("\r\n" + "RECURRINGALARMTYPE=#" + "\r\n")
            output.write("\r\n" + "RECURRINGALARMVALUE=#" + "\r\n")
            output.write("\r\n" + "ORIGINALDEST=#" + "\r\n")
            output.write("\r\n" + "SENDERCODE=6WtUIl6no8:;w`3u/tCl]MxC`p^jDJTlAHS=jo>Sn4xiJKpK#" + "\r\n")
            output.write("\r\n" + "AUTOREGISTER=#" + "\r\n")
            output.write("\r\n" + "INSERTSENTTOLIST=#" + "\r\n")
            output.write("\r\n" + "ROLLUP=#" + "\r\n")
            output.write("\r\n" + "PLAINTEXT=#" + "\r\n")
            output.write("\r\n" + "TRANSPARENCY=0#" + "\r\n")
            output.write("\r\n" + "SentToUser_V61=sandoval#" + "\r\n")
            output.write("\r\n" + "SenderIsSharingNotes_V61=1#" + "\r\n")
            output.write("\r\n" + "ChatID_V62=0#" + "\r\n")
            output.write("\r\n" + "ChatAvatarFileName_V62=#" + "\r\n")
            output.write("\r\n" + "ChatAvatarBase64Encoded_V62=#" + "\r\n")
            output.write("\r\n" + "ChatOperation_V62=0#" + "\r\n")
            output.write("\r\n" + "ChatParticipants_V62=#" + "\r\n")
            output.write("\r\n" + "HLINES_V60=0#" + "\r\n")
            output.write("\r\n" + "LMARGIN_V60=0#" + "\r\n")
            output.write("\r\n" + "GCOLOR_V60=0#" + "\r\n")
            output.write("\r\n" + "TEXTURE_V60=0#" + "\r\n")
            output.write("\r\n" + "TILESTRETCH_V60=0#" + "\r\n")

            if imageBase64 == "":
                  output.write("\r\n" + "RTF_V60={\\rtf1\\ansi\\ansicpg1252\deff0\deflang1046{\\fonttbl{\\f0\\froman\\fprq2\\fcharset0 Times New Roman;}}" + "\r\n")
                  output.write("\r\n" + "{\colortbl ;\\red0\green0\\blue0;}" + "\r\n")                  
            else:
                  output.write("\r\n" + "RTF_V60=" +  imageBase64 + "|#!ENDOF rtf tcpip#")         
        

            msgsplit = message.splitlines()

            if imageBase64 == "":       
                  for i in range(len(msgsplit)): 
                          if not  msgsplit[i]:
                              output.write("\\par" + "\r\n")
                          else:
                              output.write(msgsplit[i] + "\\par" + "\r\n")

                  output.write("\r\n" + "\\par" + "\r\n")        
                  output.write("\r\n" + "}" + "\r\n")

                  output.write("\r\n" + "ENDOF rtf tcpip#" + "\r\n")
                  if bytesattached != "":
                        output.write("\r\n" + "Attachment follows," + str(bytesattached) + "#" + "\r\n")
                        output.write( dataAttached.getvalue() + "\r\n")

            msgfinal = ""

            saveMsg(nome,ip,titulo,message)            
            try:
                  if DoesServiceExist(ip_sender[x]):
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((ip_sender[x], 39681))                  
                        client.send(output.getvalue())                        
                        client.shutdown(socket.SHUT_RDWR)
                        client.close()    
                  else:         
                        sussecs = "2"
                  
            except socket.timeout:
                  sussecs = "2"
            except socket.error:
                  sussecs = "2"
      if imageBase64 != "":
            command1 = "cd " + path_tmp + "; rm *.rtf *.png *.txt"              
            os.system(command1)

      if sussecs == "2":
            if len(ip_sender) >1:
                  msgerror = "I have not had this response!\\nTry again, or try later!";                      
            else:
                  msgerror = "Unable to send to " + nome.upper() + "\\nTry again, or try later!"
                  command = "notify-send --hint=int:transient:1 \"TurboNote Gnome3\" \"" + (msgerror).decode('iso-8859-1').encode('utf8') + "\" -i " + path_icon + "turbo.png"                  
                  os.system(command)
      else:
            msg = "Successfully sent to " + nome.upper()     
            command = "notify-send --hint=int:transient:1 \"TurboNote Gnome3\" \"" + (msg).decode('iso-8859-1').encode('utf8') + "\" -i " + path_icon + "turbo.png"
            os.system(command)

def richTextMaker(imagesrc):
            
      image = Image(imagesrc)
      outputrtf = cStringIO.StringIO()

      outputrtf.write("{\\rtf1\\ansi\\ansicpg1252\deff0\deflang1046{\\fonttbl{\\f0\\froman\\fprq6\\fcharset0 Arial;}}" + "\r\n")
      outputrtf.write("{\colortbl ;\\red0\green0\\blue0;}"  + "\r\n")
      outputrtf.write("\\viewkind4\uc1\pard\cf1\\f0\\fs20  \par"  + "\r\n")
      outputrtf.write(image.getData()  + "\r\n")        

      outputrtf.write("} \par"  + "\r\n")
      outputrtf.write(" \par"  + "\r\n")
      outputrtf.write("}"  + "\r\n")
      outputrtf.write("\00")

      f = open(path_tmp + "fullscreen.rtf", 'w')         
      f.write(outputrtf.getvalue())
      f.close()  

def saveMsg(nome,ip,titulo,message):
      data = unicode(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
      savesend = sqlite3.connect(path + 'turbo.db')
      try:
            c = savesend.cursor()
            c.execute("INSERT INTO history_send (nome,ip,texto,titulo,data) VALUES (?,?,?,?,?)",(nome,ip,message,titulo,data))
            savesend.commit()
            savesend.close()
      except:
            c = savesend.cursor()
            c.execute("INSERT INTO history_send (nome,ip,texto,titulo,data) VALUES (?,?,?,?,?)",(nome,ip,message.decode('iso-8859-1'),titulo,data))
            savesend.commit()
            savesend.close()

def DoesServiceExist(host):
      try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((host, 39681))
            s.close()
      except:
            return False

      return True    

args = sys.argv[1:]
ip = args[1]
message = args[0]
nome = args[2]
stay = args[3]
titulo = args[4]
att = args[5]
client(message,ip,nome,stay,titulo,att)