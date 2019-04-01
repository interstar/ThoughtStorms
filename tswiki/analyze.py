
import re, urllib.request, urllib.error, urllib.parse
	
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
		return self.soundcloud(self.youtube(self.bandcamp(l)))
		
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
			
	def soundcloud(self,l) :
		e1 = re.compile(r"""<iframe (.*) src="https://w.soundcloud.com/player/(.+)url=https%3A//api.soundcloud.com/tracks/([0-9]+)&amp(.*)></iframe>""")
		m = e1.match(l)
		if m :
			return """
[<SOUNDCLOUDINDIVIDUAL
id: %s
>]""" % m.group(3)
		e2 = re.compile(r"""<iframe (.*) src="https://w.soundcloud.com/player/(.+)url=https%3A//api.soundcloud.com/playlists/([0-9]+)&amp;(.*)></iframe>""")
		m = e2.match(l)
		if m :
			return """
[<SOUNDCLOUD
id: %s
>]
""" % m.group(3)
		if "soundcloud.com" in l :
			return """ Looks like you're analyzing soundcloud. Try grabbing the share / embed link and analyzing that"""
		else :
			return l


	def bandcamp(self,l) : 
		e = re.compile(r"""<iframe style="(.*)" src="https://bandcamp.com/EmbeddedPlayer/album=([0-9]+)/(.*)transparent=true/" seamless><a href="(.*)">(.*)</a></iframe>""")
		m = e.match(l)
		if m :
			return """
[<BANDCAMP
id: %s
url: %s
description: %s
>]""" % (m.group(2),m.group(4),m.group(5))
		else : 
			if "bandcamp.com" in l :
				return """
Looks like you're trying to embed a Bandcamp album. 

Try going to the Share/Embed option, choosing "Embed this Album", selecting a style and copying the embed tag.
"""
			else :
				return l


	def analyze(self,data) : 
		xs = [self.analyze_line(l) for l in data.split("\n")]
		
		return """
		<textarea name="data" cols="120" rows="30">Data Was : 
		
%s		
		</textarea>""" % "\n".join(xs)

