<html>
<head>
	<link rel="stylesheet" type="text/css"
		      href="https://fonts.googleapis.com/css?family=Inconsolata">
	<link rel="stylesheet" type="text/css" href="/static/css/main.css">

</head>

<body>
	<div class="headerbar">
		<h2>({{wikiname}}) {{pageName}}</h2>
	</div>
	<div class="menubar">
		<a href="/">HelloWorld</a> 

		% if pageStore.is_writable() :
		 | <a href="/edit/{{pageName}}">Edit this Page</a>
		% end
		</div>

		<div id="content">
		{{! body}}
	</div>

</body>
</html>
