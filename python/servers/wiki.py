
from sys import argv

from bottle import route, run, template, get, post, request, redirect, static_file

import bottle

from thoughtstorms.PageStore import PageStore, WritablePageStore
from thoughtstorms.txlib import MarkdownThoughtStorms

from services import Services, ServiceService, register_service

chef = MarkdownThoughtStorms()

# args 
# python wiki.py wikiname typecode port-no pages_dir services_dir assets_dir
wikiname, typecode, port, pages_dir, services_dir, assets_dir = argv[1],argv[2],argv[3],argv[4],argv[5],argv[6]

print """Starting Wiki :
Type   : %s
Port   : %s
Pages  : %s
Assets : %s """ % (typecode,port,pages_dir,assets_dir)

bottle.TEMPLATE_PATH.append( assets_dir )
print "Bottle Template Path : %s" % bottle.TEMPLATE_PATH
if assets_dir[-1] != "/" :
	assets_dir = assets_dir + "/"

static_root = assets_dir + "static/"
print "Static Root : %s" % static_root

# Setup PageStore
if typecode == "w" :
	page_store = WritablePageStore(pages_dir,"md")
else :
	page_store = PageStore(pages_dir,"md")
	
print "PageStore : %s" % page_store

# Setup Services
print "Services Directory : %s" % services_dir
services = Services(services_dir)
register_service(services,ServiceService)

print services.path_services

## ________________________________________________________________________

## Helpers

def make_form(current_content,wikiname,put_route,page_name,page_store) :
	return template('page',wikiname=wikiname,pageName=page_name,pageStore=page_store, body = """
<form name="wiki" action="/%s/%s" method="POST">
	<input type="submit" id="submit" name="Save Page"/>
	<input type="hidden" name="pageName" id="pageName" value="%s"/>
	<div id="input_area">
		<textarea name="body" cols="120" rows="30">%s</textarea>
	</div>
</form>""" % (put_route,page_name,page_name,current_content))


## ________________________________________________________________________
## Routing
@route('/')
def root() :
	redirect('/view/HelloWorld')


## Static files
@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root=static_root+"/css")


    
## Actions
@route('/view/<pname>')
def view(pname) :
	
	x = page_store.get(pname,lambda pname, e : "Page does not exist. Try <a href='/edit/%s'>editing</a>"%pname, lambda pname, e : "Error: %s" % e )
	body = chef.cook(x)	
	return template('page', pageName=pname,body=body,pageStore=page_store,wikiname=wikiname)

@route('/edit/<pname>')
def editor(pname) :
	x = page_store.get(pname,lambda pname, e : "New Page %s\n=====" % pname, lambda pname, e : "Error: %s" % e)	
	return make_form(x,wikiname,"put",pname,page_store)


@post('/put/<pname>')
def poster(pname) :
	body = request.forms.get("body")
	page_store.put(pname,body)
	redirect('/view/%s'%pname)



# Services
@get('/services/<sname>')
def get_service(sname) :
	if services.exists(sname) :
		s = services.find_service(sname)
		return s.process()
	else :
		return "SERVICE %s DOESN'T EXIST" % sname
	
		

if __name__ == '__main__' :
	run(host='0.0.0.0', port=port)

