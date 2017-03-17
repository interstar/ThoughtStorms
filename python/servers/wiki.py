
from sys import argv

from bottle import route, run, template, get, post, request, redirect, static_file

import bottle

from thoughtstorms.PageStore import PageStore, WritablePageStore
from thoughtstorms.txlib import MarkdownThoughtStorms


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
			self.page_store = WritablePageStore(pages_dir,"md")
		else :
			self.page_store = PageStore(pages_dir,"md")
	
		print "PageStore : %s" % self.page_store

		# Setup Services
		print "Services Directory : %s" % services_dir
		if typecode == "w" :
			self.service_page_store = WritablePageStore(services_dir,"yml")
		else :
			self.service_page_store = PageStore(services_dir,"md")
		
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
	return template('page',pageName=page_name,wikiname=wiki.wikiname,normal_page=normal,pageStore=wiki.page_store,body=body)

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
	x = wiki.page_store.get(pname,lambda pname, e : "Page does not exist. Try <a href='/edit/%s'>editing</a>"%pname, lambda pname, e : "Error: %s" % e )
	body = wiki.chef.cook(x)	
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
wiki.service_names = [["services","/service/services","List of all Services on this Wiki"], 
					  ["raw","/service/raw/HelloWorld","Raw version of a page"]]


@get('/service/services')
def get_services() :	
	services = ["""**%s**,, Example [%s](%s),, [DataPage](/sview/%s),, %s""" % (s,expl,expl,s,desc) for s,expl,desc in wiki.service_names]
	
	x = wiki.chef.cook("\n" + j(services))
	return make_page("Services",x,wiki)
	
@get('/service/raw/<pname>')
def get_raw(pname) :
	return wiki.page_store.get(pname,lambda pname, e : "Page does not exist. Try <a href='/edit/%s'>editing</a>"%pname, lambda pname, e : "Error: %s" % e )
	

		
@route('/sview/<sname>')
def view(sname) :
	x = wiki.service_page_store.get(sname,lambda pname, e : "Page does not exist. Try <a href='/sedit/%s'>editing</a>"%pname, lambda pname, e : "Error: %s" % e )
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

