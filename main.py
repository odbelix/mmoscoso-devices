#!/usr/bin/env python
# Manuel Moscoso Dominguez
#Application for IT device  management. This application store the information
#of IT devices in a mysql database with the goal to create a easy way to remote access
# Version 0.1
# 30-12-2013
# Chile, Talca.
from src.DeviceManager import DeviceManager
from src.TreeOfDevice import TreeOfDevice
from src.DBManager import DBManager
try:
  import gtk, gobject, pygtk
except:
  print >> sys.stderr, "You need to install the python gtk bindings"
  sys.exit(1)
  
# import vte
try:
  import vte
except:
  error = gtk.MessageDialog (None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
    'You need to install python bindings for libvte')
  error.run()
  sys.exit (1) 

                
class MainMobvices:
	# Global Variables
	has_vte = False
	list_type_devices = ['SW','RSW','AP','GW','ALL']
	databasefile = 'database.ini'
	database = {}

	
	#Get database information from file
	def getDataBaseInfo(self):
		global databasefile
		global database
		
		data = ConfigParser.ConfigParser()
		if os.path.exists(self.databasefile) == False:
			print "ERROR: %s not exists" % self.databasefile
			return False
		else:
			data.read(self.databasefile)
			#Put values to array
			self.database.update({'host':data.get('database','host')})
			self.database.update({'name':data.get('database','name')})
			self.database.update({'user':data.get('database','user')})
			self.database.update({'password':data.get('database','password')})
			self.database.update({'prefix':data.get('database','prefix')})
			return True
	
	#Execute query
	def selectValues(self,query):
		global database
		self.getDataBaseInfo()
		db = MySQLdb.connect(self.database['host'],self.database['user'],self.database['password'],self.database['name'])
		cursor = db.cursor()
		try:
			cursor.execute(query)
			results = cursor.fetchall()
			return results
		except MySQLdb.Error, e:
			print "An error has been passed. %s" %e
			return False
	
	def createDevice(self,widget, data=None):
		device = DeviceManager()
		
	       
	def hello(self,widget, data=None):
		print " -> %s" % str(widget)
		
	def searchByName(self,widget, data=None):
		print "Searching by name (%s)... " % self.entry_search.get_text()
		self.tree_device.set_search_entry(self.entry_search)
		self.tree_device.expand_all()
		childrens = self.tree.get_ListDevice()
		lists =  self.tree.get_ListSearch()
		lists.clear()
		print "> %s" % str(childrens)
		for child in childrens:
			if self.entry_search.get_text().lower() in child[1].lower():
				print "%s - %s" %(self.entry_search.get_text(),child[1])
				lists.append([child[0], child[1],child[2],child[3],child[4],child[5],child[6],child[7],child[8]])
		
		self.tree.set_List(lists,2)
		
				
			
	def delete_event(self, widget, event, data=None):
		gtk.main_quit()
		return False
		
		
	def destroy(self, widget, data=None):
		print "destroy signal occurred"		
		gtk.main_quit()
		
		
	def CloseVTEandRemove(self,widget, data=None):
		print "Close vte"
		global has_vte
		self.hboxrow2.remove(self.v)
		has_vte = False
	
	def getSelectedDevice(self):
		selection = self.tree_device.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		tree_model, tree_iter = selection.get_selected()
		self.selected_type = tree_model.get_value(tree_iter, 0)
		self.selected_name = tree_model.get_value(tree_iter, 1)
		self.selected_ip = tree_model.get_value(tree_iter, 2)
		self.selected_input = tree_model.get_value(tree_iter, 6)
		self.selected_username = tree_model.get_value(tree_iter, 3)
		return [self.selected_type,self.selected_name,self.selected_ip,self.selected_input,self.selected_username]

	def AddVTE(self,widget, data=None):
		print "Adding vte"
		global has_vte
		if has_vte == False:
			selection = self.tree_device.get_selection()
			selection.set_mode(gtk.SELECTION_SINGLE)
			tree_model, tree_iter = selection.get_selected()
			self.selected_type = tree_model.get_value(tree_iter, 0)
			self.selected_name = tree_model.get_value(tree_iter, 1)
			self.selected_ip = tree_model.get_value(tree_iter, 2)
			self.selected_input = tree_model.get_value(tree_iter, 6)
			self.selected_username = tree_model.get_value(tree_iter, 3)
			print "%s -> %s -> %s -> %s" % (self.selected_type,self.selected_name,self.selected_ip,self.selected_input)
			
			#Making line of execution
			if self.selected_input == 'ssh':
				command = self.selected_input+" "+self.selected_username+"@"+self.selected_ip+" \n"
			else:
				command = self.selected_input+" "+self.selected_ip+"\n"
			
			##Making VTE.
			self.v = vte.Terminal ()
			self.v.connect ("child-exited", lambda term: self.CloseVTEandRemove(self))
			self.v.fork_command()
			self.hboxrow2.pack_start(self.v,True, True, 2)
			length = len(command)
			self.v.show()
			self.v.feed_child(command,length)
			has_vte = True
		else:
			print "Vte already exists!"
			selection = self.getSelectedDevice()
			print "%s -> %s -> %s -> %s" % (selection[0],selection[1],selection[2],selection[3])
			
			#Making line of execution
			if selection[3] == 'ssh':
				command = selection[3]+" "+selection[4]+"@"+selection[2]+" \n"
			else:
				command = selection[3]+" "+selection[2]+"\n"
			
			self.v.feed_child(command,len(command))
			
	def RefreshListDevices(self,widget, data=None):
		print "Refreshing list of devices"
	
	def __init__(self):
		# create a new window
		global has_vte
		global list_type_devices
		
		
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("devices ITv0.1")
		self.window.connect("delete_event", self.delete_event)
		self.window.set_default_size(1200, 600)
		self.window.set_border_width(10)  
		
		#TreeofDevice
		self.tree = TreeOfDevice()
		
		#Class DBManager
		query = "SELECT type,name,ip,username,pass,enable,input,system_sn,model FROM device"
		db = DBManager()
		results = db.selectValues(query)
		
		self.tree.set_list_devices(results)
		self.tree_device = self.tree.create_list()
		#self.tree_device.connect('cursor-changed', self.getSelectedDevice)
		
		#Buttons
		button = gtk.Button("Salir ")
		button.connect_object("clicked", self.destroy,self.window)
		button_connect = gtk.Button("Conectar")
		button_connect.connect_object("clicked", self.AddVTE,self.window)
		button_refresh = gtk.Button("Refrescar Lista")
		button_refresh.connect_object("clicked", self.RefreshListDevices,self.window)
		
		#Buttos for CRUD device
		self.entry_search = gtk.Entry(100)
		
		
		button_search = gtk.Button("Buscar")
		button_add = gtk.Button("Agregar")
		button_delete = gtk.Button("Eliminar")
		button_update = gtk.Button("Actualizar")
		button_search.connect_object("clicked", self.searchByName,self.window)
		button_add.connect_object("clicked", self.createDevice,self.window)
		button_delete.connect_object("clicked", self.hello,self.window)
		button_update.connect_object("clicked", self.hello,self.window)
		
		
		self.hbutton_box = gtk.HButtonBox()
		self.hbutton_box.set_layout(gtk.BUTTONBOX_END)
		#self.hbutton_box.add(entry_search)
		#self.hbutton_box.add(button_search)
		self.hbutton_box.add(button_add)
		self.hbutton_box.add(button_delete)
		self.hbutton_box.add(button_update)
		#End Buttons for CRUD device
		
		
		#VBOX AND HBOX
		self.vboxmain = gtk.VBox(False, 0)
		self.hboxrow1 = gtk.HBox(False,0)
		self.hboxrow2 = gtk.HBox(True,0)
		
		#FOR TREE
		self.vboxtreeandbuttons = gtk.VBox(False,0)
		self.scrolledwindow = gtk.ScrolledWindow()
		self.scrolledwindow.add(self.tree_device)
		
		
		self.vboxtreeandbuttons.pack_start(self.scrolledwindow)
		self.vboxtreeandbuttons.pack_start(self.hbutton_box,False)
		
		self.vboxmain.pack_start(self.hboxrow1,False,False,2)
		self.vboxmain.pack_start(self.hboxrow2,True,True,2)
		
		self.window.add(self.vboxmain)
		self.hboxrow1.pack_start(button,False, False, 2)
		self.hboxrow1.pack_start(button_connect,False, False, 2)
		self.hboxrow1.pack_start(self.entry_search,False, False, 2)
		self.hboxrow1.pack_start(button_search,False, False, 2)
		self.hboxrow2.pack_start(self.vboxtreeandbuttons,True,True,2)
	
		
		#SHOW
		self.window.show_all()
		
		#DEFAULT OPTIONS
		has_vte = False

	def main(self):
		gtk.main()

print __name__

if __name__ == "__main__":
	base = MainMobvices()
	base.main()
	
	


