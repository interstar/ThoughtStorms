import random
import re
import json
import sys

import pdb

class SfwPage :
    def __init__(self,title) :
        if '/' in title : title=(title.split('/'))[-1]
        self.title = title
        self.story = []
        self.journal = []

    def randomId(self) :
        return "%08d%08d" % (random.randint(0,10**8),random.randint(0,10**8))
        
    def slug(self,s) :
        re.sub(s,'\s','-')
        re.sub(s,'\/','--')
        re.sub(s,'[^A-Za-z0-9-]','')
        s = s.lower()
        

    def para(self,data,type="paragraph") :
        s = data.encode("ascii","xmlcharrefreplace")
        return {"type":type, "id":self.randomId(), "text":s}
        
    def addPara(self,data,type="paragraph") :
        self.story.append(self.para(data,type))
        
        
    def page(self) :
        return {"title":self.title, "story":self.story, "journal":self.journal}
    
    
    def __str__(self) :
        return json.dumps(self.page(),ensure_ascii=False)
    
    
class UseMod2SFW :
    def __init__(self, fName) :

        self.page = SfwPage(fName)
        
        with open(fName) as f :
            s = f.read()
            s = s.decode("Latin1","replace")
            lines = re.split('((\r)*\n)',s)

            build = u""
            for l in lines :
                if l :
                    build = build + l
                else :
                    self.page.addPara(self.camelCaseLinks(build),"wikish")
                    build = ""
            self.page.addPara(self.camelCaseLinks(build))

    def camelCaseLinks(self,s) :
        return re.sub(u'([A-Z][a-z]+([A-Z][a-z]+)+)','[[\\1]]',s)

    def __str__(self) :              
        return self.page.__str__()
            
if __name__ == '__main__' :
    # Use like this : 
    # python importFiles.py page1 page2 page3 etc.
    # where page1 page2 page3 are plain-text files exported from your wiki
    # NOTE: you must have an "output" subdirectory of the directory where you run 
    # this script, as that's where it will write output 
   
    for v in sys.argv[1:] :
        try :
            conv = UseMod2SFW(v)
            x = u"%s" % conv
            f = open('output/%s'%(conv.page.title.lower()),'w')
            f.write(x)
            f.close()
        except Exception, e:
            print "error %s in %s" % (e, v)
            # pdb.post_mortem()
