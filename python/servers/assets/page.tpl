<html>
<head>
	<link rel="stylesheet" type="text/css"
		      href="https://fonts.googleapis.com/css?family=Inconsolata">
	<link rel="stylesheet" type="text/css" href="/static/css/main.css">

</head>

<body>
	<div class="menubar">
		<a href="/">HelloWorld</a> 
		|
		<a href="/view/RecentChanges">RecentChanges</a>

		% if pageStore.is_writable() :
		| <a href="/{{editPathName}}/{{pageName}}">Edit this Page</a>
		| <a href="javascript:(function(){%20%20%20%20%20%20%20%20/*%20Statements%20returning%20a%20non-undefined%20type,%20e.g.%20assignments%20*/%20%20%20%20%20%20%20%20%20%20%20%20window.location='http://localhost:8090/appendto/{{pageName}}/LinkBin/'+document.URL;%20%20%20%20%20%20%20%20})();">TS#{{pageName}}</a>
		% end
		|
		<a href="/service/services">Services</a>
		|
		<a href="/service/analyze">Analysis</a>
		% if pageStore.is_writable() :
    	 | <a href="/delete/{{pageName}}">Delete this Page</a>
		% end
		
	</div>

	<div class="
	% if normal_page :
headerbar
	% else :
serviceheaderbar
	% end	
	">
	
	<h2>
	% if normal_page :
		<a href="/service/search/{{pageName}}">{{pageName}}</a>
	% else :
		{{pageName}}
	% end

	<span class="wikiname">({{wikiname}})</span></h2>

	</div>


	<div id="content">
		{{! body}}
	</div>


</body>
</html>
