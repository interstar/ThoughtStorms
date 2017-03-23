
from txlib import chef
from subprocess import check_output, CalledProcessError

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
		
	def is_searchable(self) : return True
	
	def file_name_2_page_name(self,fName) :
		print fName
		r = fName.split("/")[-1]
		r = r[:-len(self.extension)-1]
		print r
		return r
			
	def search(self,text) :
		try  :
			res = check_output(["grep -i %s %s/*.%s" % (text,self.pages_dir,self.extension)], shell=True)
		except CalledProcessError, e :
			if e.returncode == 1 :
				return "No results"
		print res
		rs = res.split("\n")
		def f(l) :
			r = self.file_name_2_page_name(l.split(":")[0])			
			return "* [[%s]]" % r
		rs = sorted(set([f(r) for r in rs ]))
		print rs		
		return "\n".join(rs)

	def all_pages(self) :
		res = check_output(["ls %s/*.%s" % (self.pages_dir,self.extension)],shell=True).split("\n")		
		res = sorted(set([self.file_name_2_page_name(x) for x in res]))
		return res
		
				
class WritablePageStore(PageStore) :

	def __str__(self) :
		return "Read/Write PageStore with pages at %s" % self.pages_dir

	def is_writable(self) : return True

	def update_recent_changes(self,pName) :
		xs = self.get("RecentChanges",lambda pname, e : "", lambda pname, e : "Error %s " % e)
 		print xs
 		xs = xs.split("\n")
		
		xs = (["* [[%s]] %s" % (pName,datetime.date.today())] + xs)[:50]
		
		f = open(self.fName("recentchanges"),'w')
		f.write("\n".join(xs))
		f.close()
		

	def put(self,pName,body) :
		f = open(self.fName(pName.lower()),"w")
		f.write(body)
		f.close()
		self.update_recent_changes(pName)
	
