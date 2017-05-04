
import re
	
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
		return self.youtube(l)
		
	def youtube(self,l) :
		print "in youtube"
		print l
		e = re.compile(r"https://www.youtube.com/watch\?v=(\S+)")
		m = e.match(l)
		print m
		if m :
			print "aa ", m
			print "bb ", m.groups()
			print "cc ", m.group(1)
			return """
[<YOUTUBE
id : %s
>] """ % m.group(1)
		else : 
			return l

		
	
	def analyze(self,data) : 
		xs = [self.analyze_line(l) for l in data.split("\n")]
		
		return """
		<textarea name="data" cols="120" rows="30">Data Was : 
		
%s		
		</textarea>""" % "\n".join(xs)

