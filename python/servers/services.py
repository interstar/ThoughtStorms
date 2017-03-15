import markdown
from thoughtstorms.PageStore import WritablePageStore

class Services :
	def __init__(self,service_dir) :
		self.pageStore = WritablePageStore(service_dir,"yml")
		self.path_services = {}
		
	def add_path_service(self,sname,ps) :
		self.path_services[sname] = ps
			
	def exists(self,sname) :
		return sname in self.path_services.iterkeys()		

	def find_service(self,sname) : 
		if not self.exists(sname) : raise "Error : Service %s doesn't exist" % sname
		return self.path_services[sname] 


# the default PathService
class ServiceService :
	
	def __init__(self) :
		self.name = "ServiceService"
		self.sname = "service_service"
		self.description = """A basic service that lists the other services registered on this wiki."""

	def set_services(self,services) :
		self.services = services
		
	def process(self,*args) :
		installed = "\n".join(["""* [%s](/services/%s) : %s""" % (self.name,self.sname,self.description)])
		x = markdown.markdown("""### This is %s
		
%s
		
%s""" % (self.name,self.description,installed ))
		print x
		return x

def register_service(services,service_class) :
	s = service_class()
	services.add_path_service(s.sname,s)
	s.set_services(services)

