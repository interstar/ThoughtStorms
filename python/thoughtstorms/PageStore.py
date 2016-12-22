
from txlib import chef

class PageStore :
	
	def __init__(self,pages_dir) :
		self.pages_dir = pages_dir
	
	def __str__(self) :
		return "(ReadOnly) PageStore with pages at %s" % self.pages_dir
	
	def fName(self,pName) :
		return "%s/%s.md" % (self.pages_dir,pName)
		
	def get(self,pName) :
		file_name = self.fName(pName.lower())
		f = open(file_name)
		return f.read().decode("utf-8")
	

	def is_writable(self) : return False
	
	def put(self,pName,body) :
		raise Exception("This PageStore doesn't allow writing")
 
class WritablePageStore(PageStore) :

	def __str__(self) :
		return "Read/Write PageStore with pages at %s" % self.pages_dir

	def is_writable(self) : return True

	def put(self,pName,body) :
		f = open(self.fName(pName.lower()),"w")
		f.write(body)
		f.close()
	
