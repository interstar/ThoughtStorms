
import re, urllib2
	
class Analyzer :
	def make_form(self) :
		return """
<form name="analyze" action="/service/analyze_it" method="POST">
	<input type="submit" id="submit" name="Save Page"/>
	<div id="input_area">
		<textarea name="data" cols="120" rows="30"></textarea>
	</div>
</form>""" 

	
	def analyze_line(self,l) :
		return self.quora(self.youtube(l))
		
	def youtube(self,l) :
		e = re.compile(r"https://www.youtube.com/watch\?v=(\S+)")
		m = e.match(l)
		if m :
			return """
[<YOUTUBE
id : %s
>] """ % m.group(1)
		else : 
			return l

		
	def quora(self,l) :
		print "in quora"
		print l
		name = "Phil-Jones"
		e = re.compile(r"https://www.quora.com/(.+?)/answer/%s" % name)
		m = e.match(l)
		if m :
			response = urllib2.urlopen(l)
			html = response.read()
			
			return """
			
			%s
			 
			""" % html
		else :
			return l
	
	def analyze(self,data) : 
		xs = [self.analyze_line(l) for l in data.split("\n")]
		
		return """
		<textarea name="data" cols="120" rows="30">Data Was : 
		
%s		
		</textarea>""" % "\n".join(xs)

