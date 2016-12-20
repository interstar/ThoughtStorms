import re

## Line based 
def youtube_line(s) :
	r = re.compile("::YOUTUBE=(\S+)",re.MULTILINE)
	if r.search(s) :            
		s = r.sub(r"""<div class="youtube-embedded"><iframe width="400" height="271" src="\1" frameborder="0" allowfullscreen></iframe></div>""",s)
	return s

def soundcloud_line(s) :
	r = re.compile("::SOUNDCLOUD=(\S+)",re.MULTILINE)
	if r.search(s) :
		s = r.sub(r"""<div class="soundcloud-embedded"><iframe width="100%" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player?url=\1&amp;visual=true"></iframe></div>""",s)            
	return s

def bandcamp_line(s) :
	r = re.compile("::BANDCAMP=(\S+)\s+(\S+)\s+(.+)",re.MULTILINE)
	if r.search(s) :
		s = r.sub(r"""<div class="bandcamp-embedded"><iframe style="border: 0; width: 350px; height: 555px;" src="https://bandcamp.com/EmbeddedPlayer/album=\1/size=large/bgcol=ffffff/linkcol=0687f5/transparent=true/" seamless><a href="\2">\3</a></iframe></div>""",s)
	return s


def social_filters(s) :
	return youtube_line(soundcloud_line(bandcamp_line(s)))
		
## Standard Wikish (from UseMod)		
class WikishProcessor :

    def __init__(self) :
        self.blm = re.compile("^$")
        self.hr = re.compile("----")
        self.h6 = re.compile("^======(.+)======")
        self.h5 = re.compile("^=====(.+)=====")
        self.h4 = re.compile("^====(.+)====")
        self.h3 = re.compile("^===(.+)===")
        self.h2 = re.compile("^==(.+)==")
        self.h1 = re.compile("^=(.+)=")
        self.bold = re.compile("'''(.*?)'''")
        self.italic = re.compile("''(.*?)''")
        
        self.sqrbrkt = re.compile("(\[\[(\S+?)\]\])")
        self.extlink = re.compile("(\[(\S+)\s+(.+?)\])")

		#self.wikiword = re.compile("([A-Z][a-z]+([A-Z][a-z]+)+)")
        
        self.doubleComma = re.compile("(,,)")
        
        self.indent = 0        
        self.tableMode = False
        self.newTable = False
                 
    def line(self,l) :	
        nl = l.strip()
	   
        nl = self.blm.sub("<br/><br/>",nl)
        nl = self.hr.sub("<hr>",nl)
        nl = self.bold.sub(r"<b>\1</b>",nl)
        nl = self.italic.sub(r"<i>\1</i>",nl)

        nl = self.h6.sub(r"<h6>\1</h6>",nl)
        nl = self.h5.sub(r"<h5>\1</h5>",nl)
        nl = self.h4.sub(r"<h4>\1</h4>",nl)
        nl = self.h3.sub(r"<h3>\1</h3>",nl)
        nl = self.h2.sub(r"<h2>\1</h2>",nl)
        nl = self.h1.sub(r"<h1>\1</h1>",nl)
        nl = self.sqrbrkt.sub(r"""<a href="/view/\2">\2</a>""",nl)
        nl = self.extlink.sub(r"""<a href="\2">\3</a>""",nl)

        #nl = self.wikiword.sub(r"<a href='/view/\1' title='origin'>\1</a>",nl)        
	
        if not self.tableMode :
            if self.doubleComma.findall(nl) :
                self.tableMode = True
                self.newTable = True
        
        if self.tableMode :
            if not self.doubleComma.findall(nl) :
                nl = nl + "\n</table>"
                self.tableMode = False
            else :
                nl = self.doubleComma.sub("</td><td>",nl)
                nl = "<tr><td>"+nl+"</td></tr>"

        if self.newTable :
            nl = "<table border=1px;>\n" + nl
            self.newTable = False
            
        return nl


    def outlineFilter(self,l) :
        if l[0] != "*" :
            if self.indent > 0 :
                s = "</ul>"*(self.indent)
                self.indent = 0
                l = s + "\n" + l
            return l
        
        count = 0
        while l[count] == "*" :
            count=count+1
        meat = l[count:]

        if count == self.indent :
            return " " * (self.indent+1) + "<li>" + meat + "</li>"
        if count > self.indent :
            self.indent = self.indent + 1
            return "<ul>\n" + " " * (self.indent+1) + "<li>" + meat + "</li>"
        s = "</ul>" * (self.indent + 1 - count) + "<li>" + meat + "</li>" 
        self.indent = count
        return s




    def cook(self,p) :
        lines = (self.line(l) for l in p.split("\n"))
        lines = (self.outlineFilter(l) for l in lines)
        lines = (social_filters(l) for l in lines)        
        return "\n".join(lines)





chef = WikishProcessor()

"""
  

"""

class Wikish2Markdown(WikishProcessor) :

                 
    def line(self,l) :	
        nl = l.strip()
	   
        nl = self.blm.sub("\n",nl)
        nl = self.hr.sub("<hr>",nl)
        nl = self.bold.sub(r"**\1**",nl)
        nl = self.italic.sub(r"*\1*",nl)

        nl = self.h6.sub(r"###### \1",nl)
        nl = self.h5.sub(r"##### \1",nl)
        nl = self.h4.sub(r"#### \1",nl)
        nl = self.h3.sub(r"### \1",nl)
        nl = self.h2.sub(r"## \1",nl)
        nl = self.h1.sub(r"# \1",nl)
        
        
        #nl = self.sqrbrkt.sub(r"""<a href="/view/\2">\2</a>""",nl)

        #nl = self.wikiword.sub(r"<a href='/view/\1' title='origin'>\1</a>",nl)        
	
        if not self.tableMode :
            if self.doubleComma.findall(nl) :
                self.tableMode = True
                self.newTable = True
        
        if self.tableMode :
            if not self.doubleComma.findall(nl) :
                nl = nl + "\n</table>"
                self.tableMode = False
            else :
                nl = self.doubleComma.sub("</td><td>",nl)
                nl = "<tr><td>"+nl+"</td></tr>"

        if self.newTable :
            nl = "<table border=1px;>\n" + nl
            self.newTable = False
            
        return nl



