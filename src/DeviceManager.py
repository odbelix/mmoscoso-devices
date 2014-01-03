import gtk, gobject
class DeviceManager:
	type_device = ""
	name = ""
	ip = ""
	usernmae = ""
	password = ""
	enable = ""
	input_type = ""
	sn = ""
	model = ""
	query = ""
	
	
	def saveDevice(self, widget, data=None):
		global query
		print "adding device to database..."
		self.query = "INSERT INTO device(type,name,ip,username,pass,enable,input,system_sn,model,date_update) VALUES"
		self.query = self.query + " ('%s','%s','%s','%s','%s','%s','%s','%s','%s',NOW()) " % (self.entry_type_device.get_text(),
			self.entry_name.get_text(),
			self.entry_ip.get_text(),
			self.entry_username.get_text(),
			self.entry_password.get_text(),
			self.entry_enable.get_text(),
			self.entry_input_type.get_text(),
			self.entry_sn.get_text(),
			self.entry_model.get_text())
	
	def getQuery(self):
		global query
		return query
	
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(500, 400)
		self.window.set_title("Agregar Dispositivo")
		
		
		self.table = gtk.Table(11,2,False)
		self.title_type_device = gtk.Label("Tipo")
		self.title_ip = gtk.Label("Ip")
		self.title_name = gtk.Label("Nombre")
		self.title_ip = gtk.Label("IP")
		self.title_username = gtk.Label("Usuario")
		self.title_password = gtk.Label("Clave")
		self.title_enable = gtk.Label("enable")
		self.title_input_type = gtk.Label("Input")
		self.title_sn = gtk.Label("SN")
		self.title_model = gtk.Label("Modelo")
		
		self.button_add = gtk.Button("Agregar")
		self.button_add.connect_object("clicked", self.saveDevice,self.window)
		self.button_clear = gtk.Button("Limpiar")
		#.connect_object("clicked", self.hello,self.window)
		
		self.table.attach(self.title_type_device,0,1,0,1)
		self.table.attach(self.title_ip,0,1,1,2)
		self.table.attach(self.title_name,0,1,2,3)
		self.table.attach(self.title_ip,0,1,3,4)
		self.table.attach(self.title_username,0,1,4,5)
		self.table.attach(self.title_password,0,1,5,6)
		self.table.attach(self.title_enable,0,1,6,7)
		self.table.attach(self.title_input_type,0,1,7,8)
		self.table.attach(self.title_sn,0,1,8,9)
		self.table.attach(self.title_model,0,1,9,10)
		
		### ENTRY FOR ITEMS
		self.entry_type_device = gtk.Entry(100)
		self.entry_name = gtk.Entry(100)
		self.entry_ip = gtk.Entry(100)
		self.entry_username = gtk.Entry(100)
		self.entry_password = gtk.Entry(100)
		self.entry_enable = gtk.Entry(100)
		self.entry_input_type = gtk.Entry(100)
		self.entry_sn = gtk.Entry(100)
		self.entry_model = gtk.Entry(100)
		
		self.table.attach(self.entry_type_device,1,2,0,1)
		self.table.attach(self.entry_ip,1,2,1,2)
		self.table.attach(self.entry_name,1,2,2,3)
		self.table.attach(self.entry_ip,1,2,3,4)
		self.table.attach(self.entry_username,1,2,4,5)
		self.table.attach(self.entry_password,1,2,5,6)
		self.table.attach(self.entry_enable,1,2,6,7)
		self.table.attach(self.entry_input_type,1,2,7,8)
		self.table.attach(self.entry_sn,1,2,8,9)
		self.table.attach(self.entry_model,1,2,9,10)
		
		
		
		
		self.hbutton_box = gtk.HButtonBox()
		self.hbutton_box.set_layout(gtk.BUTTONBOX_END)
		self.hbutton_box.add(self.button_clear)
		self.hbutton_box.add(self.button_add)
		
		self.table.attach(self.hbutton_box,0,2,10,11)
		self.window.add(self.table)
		
		
		self.window.show_all()
