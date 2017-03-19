
class Analyzer :
	def make_form(self) :
		return """
<form name="analyze" action="/service/analyze_it" method="POST">
	<input type="submit" id="submit" name="Save Page"/>
	<div id="input_area">
		<textarea name="data" cols="120" rows="30"></textarea>
	</div>
</form>""" 

		
	
	def analyze(self,data) : 
		return """
		<textarea name="data" cols="120" rows="30">Data Was : 
		
%s		
		</textarea>""" % data

