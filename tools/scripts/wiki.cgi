#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import os

s = os.environ["QUERY_STRING"]
if not s :
	s = "welcome-visitors"

s = s.lower()

# Change the URL below to the URL of your Smallest Federated Wiki
url = "http://thoughtstorms.info/view/%s" % s

print "Content-type: text/html"
print
print """
<html>
<head>
<meta http-equiv="REFRESH" content="0;url=%s">
</head>
<body>
Redirecting to new site. Please <a href="%s">click here</a> if not redirected

<pre>
"""  % (url,url)

print """
</pre>

</body>
</html>

"""

