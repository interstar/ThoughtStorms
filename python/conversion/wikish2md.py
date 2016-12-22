#!/usr/bin/python2

from sys import stdin, stdout, argv

from thoughtstorms.txlib import Wikish2Markdown

chef = Wikish2Markdown()

for fName in argv[1:] :
	print fName
	oName = fName.split("/")[-1]
	print oName

	with open(fName) as f:
		with open(oName,"w") as out :
			for l in f.readlines() :
				out.write(chef.line(l)+"\n")

