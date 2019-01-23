<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css"
		      href="https://fonts.googleapis.com/css?family=Inconsolata">
	<link rel="stylesheet" type="text/css"
		      href="https://fonts.googleapis.com/css?family=Raleway">

	<link rel="stylesheet" type="text/css" href="/static/css/main.css">

</head>

<body>
	<div class="menubar">
		<a href="/">HelloWorld</a> 
		|
		<a href="/service/recentchanges">RecentChanges</a>

		% if pageStore.is_writable() :
		| <a href="/{{editPathName}}/{{pageName}}">Edit this Page</a>
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
