const Gdk = imports.gi.Gdk;
const GLib = imports.gi.GLib;
const Lang = imports.lang;
const Shell = imports.gi.Shell;
const St = imports.gi.St;
const Gio = imports.gi.Gio;
const Main = imports.ui.main;
const PanelMenu = imports.ui.panelMenu;
const PopupMenu = imports.ui.popupMenu;
const Panel = imports.ui.panel;
const MessageTray = imports.ui.messageTray;
const Gettext = imports.gettext.domain('gnome-shell-extensions');
const _ = Gettext.gettext;
const Util = imports.misc.util;
const ExtensionUtils = imports.misc.extensionUtils;
const Me = ExtensionUtils.getCurrentExtension();
const ICON_SIZE = 22;

//CONFIGURATIONS
owner = GLib.get_user_name();
path_icon = "/home/" + owner + "/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/icons/"


const MessageMenuItem = new Lang.Class({
	Name: 'MessageMenu.MessageMenuItem',
	Extends: PopupMenu.PopupBaseMenuItem,
	_init: function(app) {
		this.parent();
		this._app = app;

		this.label = new St.Label({ text:app.get_name(), style_class: 'program-label' });
		this.actor.add_child(this.label);

		this._icon = app.create_icon_texture(ICON_SIZE);
		this.actor.add_child(this._icon, { align: St.Align.END, span: -1 });
	},

	activate: function(event) {
		this._app.activate_full(-1, event.get_time());
		this.parent(event);
	}
});

const MessageMenu = new Lang.Class({
	Name: 'MessageMenu.MessageMenu',
	Extends: PanelMenu.Button,

	_init: function() {
		this.parent(0.0, "MessageMenu");
		let hbox = new St.BoxLayout({ style_class: 'panel-status-menu-box' });
		let icon = new St.Icon({ icon_name: 'mymail-symbolic',
								 style_class: 'system-status-icon' });

		hbox.add_child(icon);
		this.actor.add_child(hbox);

		this.new_note_string  = _("New note");
	    this.history_string   = _("History[R] Manager");
	    this.historys_string  = _("History[S] Manager");
	    this.contacts_string  = _("Contacts Manager");
	    this.attacheds_string = _("Attacheds");
	    this.restart_string   = _("Start Server");
	    this.stop_string      = _("Stop Server");	    
	    this.about_string     = _("By Iksws");
	
		this._evolution = null;

		this._getApps();
		this._buildMenu();
	},

	_buildMenu: function()	{

		let newLauncher = new MessageMenuItem(this._evolution);
		this.menu.addMenuItem(newLauncher);

		this.newnote_tb   =  new PopupMenu.PopupMenuItem("        "+this.new_note_string);
		this.history_tb   =  new PopupMenu.PopupMenuItem("        "+this.history_string);
		this.historys_tb  =  new PopupMenu.PopupMenuItem("        "+this.historys_string);
		this.contacts_tb  =  new PopupMenu.PopupMenuItem("        "+this.contacts_string);
		this.attacheds_tb =  new PopupMenu.PopupMenuItem("        "+this.attacheds_string);
		this.restart_tb   =  new PopupMenu.PopupMenuItem(this.restart_string);
		this.stop_tb      =  new PopupMenu.PopupMenuItem(this.stop_string);
		this.about_tb     =  new PopupMenu.PopupMenuItem(this.about_string);
		
		this.about_tb.connect('activate', Lang.bind(this, this._TbAbout));		
		this.newnote_tb.connect('activate', Lang.bind(this, this._TbNewNote));				
		this.history_tb.connect('activate', Lang.bind(this, this._TbHistory));		
		this.contacts_tb.connect('activate', Lang.bind(this, this._TbContacts));		
		this.attacheds_tb.connect('activate', Lang.bind(this, this._TbAttachdes));		
		this.restart_tb.connect('activate', Lang.bind(this, this._TbRestart));
		this.stop_tb.connect('activate', Lang.bind(this, this._TbStop));		
		this.historys_tb.connect('activate', Lang.bind(this, this._TbHistorys));		

		this.menu.addMenuItem(this.newnote_tb);
		this.menu.addMenuItem(this.attacheds_tb);
		this.menu.addMenuItem(this.contacts_tb);	
		this.menu.addMenuItem(this.history_tb);
		this.menu.addMenuItem(this.historys_tb);
		this.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());
		this.menu.addMenuItem(this.restart_tb);		
		this.menu.addMenuItem(this.stop_tb);		
		this.menu.addMenuItem(this.about_tb);	

	},

	_getApps: function() {
		let appsys = Shell.AppSystem.get_default();				
		let app = appsys.lookup_app('turbonote.desktop');
		this._evolution = app;				
	},

	_TbExeDesign: function() {
		try{
		 	Main.Util.trySpawnCommandLine('firefox "http://www.exedesignsolutions.com/" &');
		 }catch(Execption){
		 	notifyTray("ERROR",Execption); 
		 }
	},
	_TbContacts: function() {
		try{
		 	Main.Util.trySpawnCommandLine('python /home/' + owner + '/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/contacts.py');
		 }catch(Execption){
		 	notifyTray("ERROR",Execption); 
		 }
	},

	_TbNewNote: function() {
		try{
		 	Main.Util.trySpawnCommandLine('python /home/' + owner + '/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/new_note.py');
		 }catch(Execption){
		 	notifyTray("ERROR",Execption); 
		 }
	},

	_TbHistory: function() {
		try{			
		 	Main.Util.trySpawnCommandLine('python /home/' + owner + '/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/historic.py');
		 }catch(Execption){		 	
		 	notifyTray("ERROR",Execption); 
		 }
	},
	_TbHistorys: function() {
		try{			
		 	Main.Util.trySpawnCommandLine('python /home/' + owner + '/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/historics.py');
		 }catch(Execption){		 	
		 	notifyTray("ERROR",Execption); 
		 }
	},
	_TbAttachdes: function() {
		try{			
		 	Main.Util.trySpawnCommandLine('python /home/' + owner + '/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/attacheds.py');
		 }catch(Execption){		 	
		 	notifyTray("ERROR",Execption); 
		 }
	},
	_TbStop: function() {
		try{			
		 	Main.Util.trySpawnCommandLine('fuser -n tcp -k 39681');		 	
		 	notifyTray("Turnbo Note Gnome 3","Server stop successful!")
		 }catch(Execption){		 	
		 	notifyTray("ERROR",Execption); 
		 }
	},	
	_TbRestart: function() {
		try{			
		 	Util.spawn(['/home/' + owner + '/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/server.py'])
		 	notifyTray("Turnbo Note Gnome 3","Server start successful!")
		 }catch(Execption){		 	
		 	notifyTray("ERROR",Execption); 
		 }
	},	
	
	_TbAbout: function() {
		Main.Util.trySpawnCommandLine('python /home/' + owner + '/.local/share/gnome-shell/extensions/turbonote@iksws.com.br/turbonote-adds/about.py');
	},

	destroy: function() {
		this.parent();
	},

});

function notifyTray(_title,_msg) {	
	Main.Util.trySpawnCommandLine("notify-send --hint=int:transient:1 '" + _title + "' '"+ _msg + "' -i '" + path_icon + "turbo.png" + "'");
}

function notifyZenity(_type,_msg){
	Main.Util.trySpawnCommandLine('zenity --' + _type+ ' --text "'+ _msg+'"');
}

function init(extensionMeta) {	
	let theme = imports.gi.Gtk.IconTheme.get_default();
	theme.append_search_path(extensionMeta.path + "/icons");
}

let _indicator;
let settings;
let originalUpdateCount;
let originalStyle;
let iconChanged = false;
let availableNotifiers = new Array ();
let statusArea;
let iconBox;

function enable() {
	_indicator = new MessageMenu;	
	statusArea =  Main.panel.statusArea;
	Main.panel.addToStatusArea('messageMenu', _indicator,1);
	iconBox =  statusArea.messageMenu.actor;
	originalStyle = iconBox.get_style(); 	
	
}

function disable() {	
	_indicator.destroy();
}
