import re, markdown


## Line based 

r_youtube = re.compile("::YOUTUBE=(\S+)",re.MULTILINE)
r_soundcloud = re.compile("::SOUNDCLOUD=(\S+)",re.MULTILINE)
r_bandcamp = re.compile("::BANDCAMP=(\S+)\s+(\S+)\s+(.+)",re.MULTILINE)
r_sqrwiki = re.compile("(\[\[(\S+?)\]\])")

def youtube_line(s) :
	if r_youtube.search(s) :            
		s = r_youtube.sub(r"""<div class="youtube-embedded"><iframe width="400" height="271" src="\1" frameborder="0" allowfullscreen></iframe></div>""",s)
	return s

def soundcloud_line(s) :
	if r_soundcloud.search(s) :
		s = r_soundcloud.sub(r"""<div class="soundcloud-embedded"><iframe width="100%" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player?url=\1&amp;visual=true"></iframe></div>""",s)            
	return s

def bandcamp_line(s) :
	if r_bandcamp.search(s) :
		s = r_bandcamp.sub(r"""<div class="bandcamp-embedded"><iframe style="border: 0; width: 350px; height: 555px;" src="https://bandcamp.com/EmbeddedPlayer/album=\1/size=large/bgcol=ffffff/linkcol=0687f5/transparent=true/" seamless><a href="\2">\3</a></iframe></div>""",s)
	return s

def sqrwiki_line(s) :
	if r_sqrwiki.search(s) :
		s = r_sqrwiki.sub(r"""<a href="/view/\2">\2</a>""",s)
	return s

class DoubleCommaTabler :

	def __init__(self) :
		self.tableMode = False
		self.newTable = False
		self.doubleComma = re.compile("(,,)")
		
	def __call__(self,l) :
		if not self.tableMode :
			if self.doubleComma.findall(l) :
				self.tableMode = True
				self.newTable = True
        
		if self.tableMode :
			if not self.doubleComma.findall(l) :
				l = l + "\n</table>"
				self.tableMode = False
			else :
				l = self.doubleComma.sub("</td><td>",l)
				l = "<tr><td>"+l+"</td></tr>"

		if self.newTable :
			l = "<table border=1px;>\n" + l
			self.newTable = False
			
		return l
		
table_line = DoubleCommaTabler()

def social_filters(s) : return youtube_line(soundcloud_line(bandcamp_line(s)))

def wiki_filters(s) : 
	return sqrwiki_line(table_line(s))

		
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
        self.extlink = re.compile("(\[(http\S+)\s+(.+?)\])")

		#self.wikiword = re.compile("([A-Z][a-z]+([A-Z][a-z]+)+)")
        
        
        self.indent = 0        
                 
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
        lines = (self.line(wiki_filters(l)) for l in p.split("\n"))
        lines = (self.outlineFilter(l) for l in lines)
        lines = (social_filters() for l in lines)        
        return "\n".join(lines)





chef = WikishProcessor()

class MarkdownThoughtStorms :
	
	def cook(self,p) :
		lines = (wiki_filters(l) for l in p.split("\n"))
		lines = (social_filters(l) for l in lines)
		page = markdown.markdown("\n".join(lines))                
		return page


class Wikish2Markdown(WikishProcessor) :

	def __init__(self,convert_tables=False) :
		WikishProcessor.__init__(self)
		self.convert_tables = convert_tables
                 
	def line(self,l) :	
		nl = l.strip()
		nl = self.blm.sub("\n",nl)
        
		nl = self.bold.sub(r"**\1**",nl)
		nl = self.italic.sub(r"*\1*",nl)

		nl = self.h6.sub(r"###### \1",nl)
		nl = self.h5.sub(r"##### \1",nl)
		nl = self.h4.sub(r"#### \1",nl)
		nl = self.h3.sub(r"### \1",nl)
		nl = self.h2.sub(r"## \1",nl)
 		nl = self.h1.sub(r"# \1",nl)
        
 		nl = self.extlink.sub(r"""[\3](\2)""",nl)
              

		if self.convert_tables :
			if not self.tableMode :
			    if self.doubleComma.findall(nl) :
			        self.tableMode = True
			        self.newTable = True
			
			if self.tableMode :
			    if not self.doubleComma.findall(nl) :
			        nl = nl + "\n\n"
			        self.tableMode = False
			    else :
			        nl = self.doubleComma.sub(" | ",nl)
			        nl = "| "+nl+" |\n"

			if self.newTable :
			    nl = "| " + nl
			    self.newTable = False

		return nl


