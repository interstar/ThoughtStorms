
from txlib import chef
import datetime

class PageStore :
	
	def __init__(self,pages_dir,extension) :
		self.pages_dir = pages_dir
		self.extension = extension
	
	def __str__(self) :
		return "(ReadOnly) PageStore with pages at %s" % self.pages_dir
	
	def fName(self,pName) :
		return "%s/%s.%s" % (self.pages_dir,pName,self.extension)
		
	def get(self,pName,no_file_handler,other_error_handler) :
		file_name = self.fName(pName.lower())
		try :
			with open(file_name) as f :
				return f.read().decode("utf-8")
		except Exception, e :
			if "No such file or directory:" in "%s"%e :
				return no_file_handler(pName,e)
			else :
				return other_error_handler(pName,e)
		

	def is_writable(self) : return False
	
	def put(self,pName,body) :
		raise Exception("This PageStore doesn't allow writing")
 
class WritablePageStore(PageStore) :

	def __str__(self) :
		return "Read/Write PageStore with pages at %s" % self.pages_dir

	def is_writable(self) : return True

	def update_recent_changes(self,pName) :
		f = open(self.fName("recentchanges"))
		xs = f.readlines()
		f.close()

		xs = (["* [[%s]] %s\n" % (pName,datetime.date.today())] + xs)[:50]
		
		f = open(self.fName("recentchanges"),'w')
		f.write("".join(xs))
		f.close()
		

	def put(self,pName,body) :
		f = open(self.fName(pName.lower()),"w")
		f.write(body)
		f.close()
		self.update_recent_changes(pName)
	
