const Applet = imports.ui.applet;
const GLib = imports.gi.GLib;
const GObject = imports.gi.GObject;
const Lang = imports.lang;
const NMClient = imports.gi.NMClient;
const St = imports.gi.St;
const Main = imports.ui.main;
const PopupMenu = imports.ui.popupMenu;
const MessageTray = imports.ui.messageTray;
const Util = imports.misc.util;


owner = GLib.get_user_name();
path_icon = "/usr/share/cinnamon/applets/turbonote@iksws.com.br/icons/"
path = "/usr/share/cinnamon/applets/turbonote@iksws.com.br/"

function MyApplet(metadata, orientation, panel_height) {
    this._init(metadata, orientation, panel_height);
}

MyApplet.prototype = {
    __proto__: Applet.IconApplet.prototype,

    _init: function(metadata, orientation, panel_height) {        
        Applet.IconApplet.prototype._init.call(this, orientation, panel_height);
        
        try {
            this.metadata = metadata;
            Main.systrayManager.registerRole("TurboNote", metadata.uuid);

            this.menuManager = new PopupMenu.PopupMenuManager(this);
            this.menu = new Applet.AppletPopupMenu(this, orientation);
            this.menuManager.addMenu(this.menu);            
            
            //this._currentIconName = undefined;
            //this._setIcon('network-offline');	   
	    this.set_applet_icon_path(path_icon+"mymail-symbolic.svg");
            this.set_applet_tooltip(_("Cinnamon TurboNote"));

            this._client = NMClient.Client.new();
            this._statusSection = new PopupMenu.PopupMenuSection();
            this._statusSection.actor.hide();

            this.menu.addMenuItem(this._statusSection);
            this.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());

	    this.menu.addAction(_("New Note"), Lang.bind(this, function() {
				Util.spawnCommandLine("python /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/new_note.py");
            }));
	    this.menu.addAction(_("Contacts Manager"), Lang.bind(this, function() {
				Util.spawnCommandLine("python /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/contacts.py");
            }));
	    this.menu.addAction(_("History Received Manager"), Lang.bind(this, function() {
				Util.spawnCommandLine("python /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/historic.py");
            }));
	    this.menu.addAction(_("History Sent Manager"), Lang.bind(this, function() {
				Util.spawnCommandLine("python /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/historics.py");
            }));
	    this.menu.addAction(_("Attacheds"), Lang.bind(this, function() {
				Util.spawnCommandLine("python /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/attacheds.py");
            }));
	    this.menu.addAction(_("Start Server"), Lang.bind(this, function() {
		 try{			
		 	Util.trySpawnCommandLine('python /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/server.py')
		 	notifyTray("Turnbo Note Gnome 3","Server start successful!")
		 }catch(Execption){		 	
		 	notifyTray("ERROR",Execption); 
		 }				
            }));
	    this.menu.addAction(_("Stop Server"), Lang.bind(this, function() {
		 try{			
		 	Util.trySpawnCommandLine('fuser -n tcp -k 39681');		 	
		 	notifyTray("Turnbo Note Gnome 3","Server stop successful!")
		 }catch(Execption){		 	
		 	notifyTray("ERROR",Execption); 
		 }
            }));
	    this.menu.addAction(_("SVN Update"), Lang.bind(this, function() {
				Util.spawnCommandLine("python /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/svnupdate.py");
            }));
            this.menu.addAction(_("About"), Lang.bind(this, function() { 
		Util.spawnCommandLine("python /usr/share/cinnamon/applets/turbonote@iksws.com.br/turbonote-adds/about.py");
	    }));
                                     
            
        }
        catch (e) {
            global.logError(e);
        }
    },
    
    _setIcon: function(name) {
        if (this._currentIconName !== name) {
            this.set_applet_icon_symbolic_name(name);
            this._currentIconName = name;
        }
    },
    
    on_applet_clicked: function(event) {
        this.menu.toggle();        
    },

    on_applet_removed_from_panel: function() {
        Main.systrayManager.unregisterRole("TurboNote", this.metadata.uuid);
        if (this._periodicTimeoutId){
            Mainloop.source_remove(this._periodicTimeoutId);
        }
    },

};

function notifyTray(_title,_msg) {	
	Util.trySpawnCommandLine("notify-send --hint=int:transient:1 '" + _title + "' '"+ _msg + "' -i '" + path_icon + "turbo.png" + "'");
}


function main(metadata, orientation, panel_height) {  
    let myApplet = new MyApplet(metadata, orientation, panel_height);
    return myApplet;      
}
