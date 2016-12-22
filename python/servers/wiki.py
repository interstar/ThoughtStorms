
from sys import argv

from bottle import route, run, template, get, post, request, redirect, static_file

import bottle

from thoughtstorms.PageStore import PageStore, WritablePageStore
from thoughtstorms.txlib import MarkdownThoughtStorms

chef = MarkdownThoughtStorms()

wikiname, typecode, port, pages_dir, assets_dir = argv[1],argv[2],argv[3],argv[4],argv[5]

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

if typecode == "w" :
	page_store = WritablePageStore(pages_dir)
else :
	page_store = PageStore(pages_dir)
	
print "PageStore : %s" % page_store

## Rerouting
@route('/')
def root() :
	redirect('/view/HelloWorld')


## Static files
@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root=static_root+"/css")
    
## Actions
@route('/view/<pname>')
def index(pname) :
	try :
		body = chef.cook(page_store.get(pname))	
	except Exception, e:
		if "No such file or directory:" in "%s"%e :
			body = "Page does not exist. Try <a href='/edit/%s'>editing</a>"%pname
		else :
			body = "Error: %s" % e
	return template('page', pageName=pname,body=body,pageStore=page_store,wikiname=wikiname)

@route('/edit/<pname>')
def editor(pname) :
	try :
		x = page_store.get(pname)
	except Exception, e:
		if "No such file or directory:" in "%s"%e :
			x = "New Page\n====="
		else :
			x = "Error: %s" % e

	return template('page',wikiname=wikiname,pageName=pname,pageStore=page_store, body = """
<form name="wiki" action="/put/%s" method="POST">
	<input type="submit" id="submit" name="Save Page"/>
	<input type="hidden" name="pageName" id="pageName" value="%s"/>
	<div id="input_area">
		<textarea name="body" cols="120" rows="30">%s</textarea>
	</div>
</form>""" % (pname,pname,x))

@post('/put/<pname>')
def poster(pname) :
	body = request.forms.get("body")
	page_store.put(pname,body)
	redirect('/view/%s'%pname)
		

if __name__ == '__main__' :
	run(host='0.0.0.0', port=port)

