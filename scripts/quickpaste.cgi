#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import os
import SFWTools

#s = os.environ["QUERY_STRING"]

form = cgi.FieldStorage()
title = form.getvalue("title","")
page = form.getvalue("page", "(no page)")
paragraph = form.getvalue("paragraph","paragraph")

if (title=="") :
  print """Content-type: text/html

<html>
<body>
<form method="POST">
Title : <input name="title"/>
<br/>
Paragraphs :
<input type="radio" name="paragraph" value="paragraph" checked/> Plain
<input type="radio" name="paragraph" value="wikish"/> Wikish
<br/>
Body :<br/>
<textarea name="page" rows="30" cols="80">
</textarea>
<br/>
<input type="submit"/>
</form>
"""
else :
  conv = SFWTools.UseMod2SFW(title, page, paragraph)

  print """Content-type: text/json
Content-Disposition: attachment; filename=%s;

%s""" % (conv.makeFileName(),"%s"%conv)

