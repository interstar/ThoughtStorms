
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
		return self.youtube(self.bandcamp(l))
		
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

	def bandcamp(self,l) : 
		e = re.compile(r"""<iframe style="border: 0; width: 350px; height: 470px;" src="https://bandcamp.com/EmbeddedPlayer/album=([0-9]+)/(.*)transparent=true/" seamless><a href="(.*)">(.*)</a></iframe>""")
		m = e.match(l)
		if m :
			return """
[<BANDCAMP
id: %s
url: %s
description: %s
>]""" % (m.group(1),m.group(3),m.group(4))

	def analyze(self,data) : 
		xs = [self.analyze_line(l) for l in data.split("\n")]
		
		return """
		<textarea name="data" cols="120" rows="30">Data Was : 
		
%s		
		</textarea>""" % "\n".join(xs)

