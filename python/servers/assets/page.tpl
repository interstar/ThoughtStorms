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
		 | <a href="/edit/{{pageName}}">Edit this Page</a>
		% end
		|
		<a href="/service/service_service">Services</a>
		
	</div>

	<div class="
	% if normal_page :
headerbar
	% else :
serviceheaderbar
	% end	
	">
		<h2>({{wikiname}}) {{pageName}}</h2>
	</div>

	<div id="content">
		{{! body}}
	</div>


</body>
</html>
