import json, sys

for fName in sys.argv[1:] :
	print fName
	pName = fName.split("/")[-1]
	print pName
	if pName == "pagelist" : 
		continue
	oName = pName.lower() + ".md"
	print oName
	
	with open(fName) as json_data:
		d = json.load(json_data)
		#print(d)
		title = d["title"]
		story = d["story"]
		
		print title
		
		with open(oName,'w') as outfile :		
			for p in story :
				print p["type"]
				if not p["type"] in ["factory","image","changes","chart"] :
					print p["text"]
					outfile.write(p["text"].encode("utf-8"))
				outfile.write("\n\n")
		

	print "____________________________________________________________"
	#break
	
