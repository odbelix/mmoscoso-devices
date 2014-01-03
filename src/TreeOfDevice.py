#TreeOfDevice: This class has the responsibility to create a Treeview 
# for view device information
# Manuel Moscoso Dominguez
# 03-01-2014
import gtk, gobject

class TreeOfDevice:
	list_devices = []
	liststore = gtk.ListStore(str, str, str, str, str, str, str, str, str)
	listsearch = gtk.ListStore(str, str, str, str, str, str, str, str, str)
	
	def set_list_devices(self,results):
		global list_devices
		list_devices = results
		
	def get_ListDevice(self):
		global liststore
		return self.liststore
	
	def get_ListSearch(self):
		global listsearch
		return self.listsearch
		
	# Change view of treeview	
	def set_List(self,lists,option):
		global listsearch
		global liststore
		#Option 1 = List completed
		if option == 1:
			#self.liststore = gtk.ListStore(str, str, str, str, str, str, str, str, str)
			self.modelfilter = self.liststore.filter_new()
			self.treeview.set_model(self.modelfilter)
		else:
			listsearch = lists
			#self.liststore = gtk.ListStore(str, str, str, str, str, str, str, str, str)
			self.modelfilter = self.listsearch.filter_new()
			self.treeview.set_model(self.modelfilter)
	
	def create_list(self):
		global list_devices
		global liststore
		
		self.treeview = gtk.TreeView()
		# create the TreeViewColumns to display the data
		self.treeview.columns = [None]*9
		self.treeview.columns[0] = gtk.TreeViewColumn('Tipo')
		self.treeview.columns[1] = gtk.TreeViewColumn('Nombre')
		self.treeview.columns[2] = gtk.TreeViewColumn('Direccion IP')
		self.treeview.columns[3] = gtk.TreeViewColumn('Usuario')
		self.treeview.columns[4] = gtk.TreeViewColumn('Password')
		self.treeview.columns[5] = gtk.TreeViewColumn('Enable')
		self.treeview.columns[6] = gtk.TreeViewColumn('Metodo Ingreso')
		self.treeview.columns[7] = gtk.TreeViewColumn('S/N')
		self.treeview.columns[8] = gtk.TreeViewColumn('Modelo')
		
		self.treeview.columns[0].set_max_width(40)
		self.treeview.columns[1].set_max_width(250)
		self.treeview.columns[2].set_max_width(250)
		self.treeview.columns[3].set_max_width(250)
		self.treeview.columns[4].set_max_width(250)
		self.treeview.columns[5].set_max_width(250)
		self.treeview.columns[6].set_max_width(250)
		self.treeview.columns[7].set_max_width(250)
		self.treeview.columns[8].set_max_width(250)
		
        
		#self.liststore = gtk.ListStore(str, str, str, str, str, str, str, str, str)
		self.modelfilter = self.liststore.filter_new()
		
		for line in list_devices:
			self.liststore.append([line[0], line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8]])
		        
		self.treeview.set_model(self.modelfilter)
		
		# add columns to treeview
		for n in range(9):
			self.treeview.append_column(self.treeview.columns[n])
			self.treeview.columns[n].cell = gtk.CellRendererText()
			self.treeview.columns[n].pack_start(self.treeview.columns[n].cell,
                                                True)
			self.treeview.columns[n].set_attributes(
				self.treeview.columns[n].cell, text=n)

        # make treeview searchable
		self.treeview.set_search_column(0)
		self.treeview.set_search_column(1)
		self.treeview.set_search_column(2)
		self.treeview.set_enable_search(True) 

		return self.treeview
