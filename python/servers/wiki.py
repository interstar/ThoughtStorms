
from sys import argv

from bottle import route, run, template, get, post, request, redirect, static_file, response

import bottle, yaml

from thoughtstorms.PageStore import PageStore, WritablePageStore
from thoughtstorms.txlib import MarkdownThoughtStorms

from analyze import Analyzer

class TSWiki :
	def __init__(self, wikiname, typecode, port, pages_dir, services_dir, assets_dir) :
		self.wikiname = wikiname
		self.port = port
		self.chef = MarkdownThoughtStorms()
		print """Starting Wiki :
		Type   : %s
		Port   : %s
		Pages  : %s
		Assets : %s """ % (typecode,port,pages_dir,assets_dir)

		bottle.TEMPLATE_PATH.append( assets_dir )
		print "Bottle Template Path : %s" % bottle.TEMPLATE_PATH
		if assets_dir[-1] != "/" :
			assets_dir = assets_dir + "/"

		self.static_root = assets_dir + "static/"
		print "Static Root : %s" % self.static_root

		# Setup PageStore
		if typecode == "w" :
			self.page_store = WritablePageStore(pages_dir,"md",lc=True,recent_changes=True)
		else :
			self.page_store = PageStore(pages_dir,"md",lc=True)
	
		print "PageStore : %s" % self.page_store

		# Setup Services
		print "Services Directory : %s" % services_dir
		if typecode == "w" :
			self.service_page_store = WritablePageStore(services_dir,"yml")
		else :
			self.service_page_store = PageStore(services_dir,"yml")

	def get_sister_sites(self) :
		sispage = self.service_page_store.get("sister_sites",lambda pname, e : "",lambda pname, e : "Error %s" % e)
		if sispage != "" :
			self.sister_sites = yaml.load(sispage)
		else :
			self.sister_sites = {}				
		return self.sister_sites
		
# args 
# python wiki.py wikiname typecode port-no pages_dir services_dir assets_dir
#wikiname, typecode, port, pages_dir, services_dir, assets_dir = argv[1],argv[2],argv[3],argv[4],argv[5],argv[6]

wiki = TSWiki(argv[1],argv[2],argv[3],argv[4],argv[5],argv[6])




## ________________________________________________________________________

## Helpers

def j(xs) : return "\n".join(xs)	

def make_form(current_content,put_route,page_name) :
	return """
<form name="wiki" action="/%s/%s" method="POST">
	<input type="submit" id="submit" name="Save Page"/>
	<input type="hidden" name="pageName" id="pageName" value="%s"/>
	<div id="input_area">
		<textarea name="body" cols="120" rows="30">%s</textarea>
	</div>
</form>""" % (put_route,page_name,page_name,current_content)


def make_page(page_name, body, wiki,normal=True) :
	if normal :
		edit_path_name = "edit"
	else: 
		edit_path_name = "sedit"
	return template('page',pageName=page_name,wikiname=wiki.wikiname, normal_page=normal,editPathName=edit_path_name, pageStore=wiki.page_store,body=body)

## ________________________________________________________________________
## Routing
@route('/')
def root() :
	redirect('/view/HelloWorld')


## Static files
@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root=wiki.static_root+"/css")

    
## Actions
@route('/view/<pname>')
def view(pname) :
	if wiki.page_store.is_writable() :
		msg = "Page does not exist. Try <a href='/edit/%s'>editing</a>"%pname
	else :
		msg = "Page does not exist."
	x = wiki.page_store.get(pname,lambda pname, e : msg, lambda pname, e : "Error: %s" % e )
	ss = wiki.get_sister_sites()
	body = wiki.chef.cook(x,ss)
	return make_page(pname, body, wiki)

@route('/edit/<pname>')
def editor(pname) :
	x = wiki.page_store.get(pname,lambda pname, e : "New Page %s\n=====" % pname, lambda pname, e : "Error: %s" % e)	
	return make_page(pname, make_form(x,"put",pname), wiki)


@post('/put/<pname>')
def poster(pname) :
	body = request.forms.get("body")
	wiki.page_store.put(pname,body)
	redirect('/view/%s'%pname)


# Services
wiki.service_names = [["services","/service/services","List of all Services on this wiki"], 
					  ["all","/service/all","List of all Pages in this wiki"],
					  ["all raw","/service/all_raw","List of all Pages in raw text"],
					  ["raw","/service/raw/HelloWorld","Raw version of a page"],
					  ["analyze","/service/analyze","Analyze a link to derive embeddable form and other useful data"],
					  ["sister_sites","","Sister sites are defined on the data-page, and used in double-square links"],
					  ["search","/service/search/HelloWorld","Crude grep for text in pages"]
					  ]


@get('/service/services')
def get_services() :	
	services = ["""**%s**,, Example [%s](%s),, [DataPage](/sview/%s),, %s""" % (s,expl,expl,s,desc) for s,expl,desc in wiki.service_names]

	ss = wiki.get_sister_sites()
	x = wiki.chef.cook("\n" + j(services),ss)
	return make_page("Services",x,wiki)
	
@get('/service/raw/<pname>')
def get_raw(pname) :
	response.content_type="text/text"
	return wiki.page_store.get(pname,lambda pname, e : "Page does not exist. Try <a href='/edit/%s'>editing</a>"%pname, lambda pname, e : "Error: %s" % e )
	
analyzer = Analyzer()

@get('/service/analyze')
def get_analyze() :
	return make_page("Analyzer",analyzer.make_form(),wiki, False)
	
@post('/service/analyze_it')
def analyze() :
	data = request.forms.get("data")
	return make_page("Analysis",analyzer.analyze(data),wiki, False)
	
@get('/service/search/<text>')
def get_search(text) :
	if not wiki.page_store.is_searchable() :
		out = "This PageStore is not searchable"
	else : 
		out = wiki.page_store.search(text)
	ss = wiki.get_sister_sites()
	out = wiki.chef.cook(out,ss)
	return make_page("Search Result for %s" % text,  out , wiki, False)

@get('/service/all')
def get_all() :
	out = "\n".join(["* [[%s]]" % p for p in wiki.page_store.all_pages()])
	ss = wiki.get_sister_sites()
	out = wiki.chef.cook(out,ss)
	return make_page("All Pages", out, wiki, False)
	
@get('/service/all_raw')
def get_all_raw() :
	response.content_type="text/text"
	return "\n".join(wiki.page_store.all_pages())

@route('/sview/<sname>')
def view(sname) :
	x = wiki.service_page_store.get(sname,lambda pname, e : "Page does not exist. Try <a href='/sedit/%s'>editing</a>"%pname, lambda pname, e : "Error: %s" % e )
	x = "<pre>%s</pre>"%x
	return make_page(sname, x, wiki, False)

@route('/sedit/<sname>')
def editor(sname) :
	x = wiki.service_page_store.get(sname,lambda pname, e : "Data for Service %s\n=====" % pname, lambda pname, e : "Error: %s" % e)	
	return make_page(sname, make_form(x,"sput",sname), wiki, False)


@post('/sput/<sname>')
def poster(sname) :
	body = request.forms.get("body")
	wiki.service_page_store.put(sname,body)
	redirect('/sview/%s'%sname)
	
	
	

if __name__ == '__main__' :
	run(host='0.0.0.0', port=wiki.port)

