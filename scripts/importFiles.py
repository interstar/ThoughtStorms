import random
import re
import json
import sys

import pdb

class SfwPage :
    # Represents a Smallest Federated Wiki Page
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
    

    def removeBlankParas(self) :
        self.story = [x for x in self.story if re.search('\S',x["text"])]
    
    def __str__(self) :
        return json.dumps(self.page(),ensure_ascii=False)
    


def splitter(criteria,page) :
    # splits page by criteria, yields each piece
    i = 0
    l = ""        
    while (i < len(page)) :
        if criteria(page,i) :
            yield l
            l = page[i]
        else :
            l = l + page[i]
        i=i+1
    yield l


def outlineSplitterFactory() :
    osFlag = [False]
    def g(chunk,i) :
        if i == len(chunk)-1 : return False
        if (chunk[i]=='\n') :
            if (osFlag[0]) :
                if (chunk[i+1]=='*') :
                    osFlag[0] = False       
                    return True
                else :
                    if (chunk[i+1]=='\n') :
                        return True
            else :
                if (chunk[i+1]!='*') :
                    osFlag[0] = True
                    return True
        return False
    return g

class UseMod2SFW :
    def __init__(self, fName) :

        self.addPage(fName)
                
        with open(fName) as f :
            s = f.read()
            s = s.decode("Latin1","replace")
            # remove \r
            s = s.replace('\r','\n')
            self.parseBody(s)

    def addPage(self,fName) :
        """ We can override this in subclasses"""
        self.page = SfwPage(fName)
    

    def parseBody(self,s) :
        build = u""
        try :
            for block in (splitter(outlineSplitterFactory(),s)) :                    
                if block :
                    self.page.addPara(self.process(block.strip()),"wikish")
        except Exception, e:
            print "error %s in %s" % (e, v)
            pdb.post_mortem()

        self.page.removeBlankParas()
    

    def process(self,s) :
        return self.camelCaseLinks(self.externalLinks(s))
                
    def camelCaseLinks(self,s) :
        return re.sub(u'(\s)([A-Z][a-z]+([A-Z][a-z]*)+)','\\1[[\\2]]',s)

    def externalLinks(self,s) :
        s = re.sub(u'(http://[\S]+\.[\S]+.[\S]+[\S]*)','[\\1 \\1]',s)
        s = re.sub(u'(https://[\S]+\.[\S]+.[\S]+[\S]*)','[\\1 \\1]',s)
        s = re.sub(u'(ftp://[\S]+\.[\S]+.[\S]+[\S]*)','[\\1 \\1]',s)
        s = re.sub(u'(ftps://[\S]+\.[\S]+.[\S]+[\S]*)','[\\1 \\1]',s)
        return s
        
    
    def __str__(self) :              
        return self.page.__str__()
        
    def makeFileName(self) :
        return self.page.title.lower()
            

class SdiDesk2SFW (UseMod2SFW):
    """ Almost like UseMod but has to strip first couple of lines"""

    def addPage(self,fName) :
        fName = fName.split('.')[0]
        self.page = SfwPage(fName)

    def parseBody(self,s) :
        build = u""
            
        try :
            count = 0
            for block in (splitter(outlineSplitterFactory(),s)) :
                if count < 5 :
                    count=count+1
                    continue
                print block
                if block :
                    self.page.addPara(self.process(block.strip()),"wikish")
        except Exception, e:
            print "error %s in %s" % (e, v)
            pdb.post_mortem()

        self.page.removeBlankParas()



            
if __name__ == '__main__' :
    # Use like this : 
    # python importFiles.py page1 page2 page3 etc.
    # where page1 page2 page3 are plain-text files exported from your wiki
    # NOTE: you must have an "output" subdirectory of the directory where you run 
    # this script, as that's where it will write output 
   
    for v in sys.argv[1:] :
        try :
            conv = UseMod2SFW(v)
            #conv = SdiDesk2SFW(v)
            x = u"%s" % conv
            f = open('output/%s'%(conv.makeFileName()),'w')
            f.write(x)
            f.close()
        except Exception, e:
            print "error %s in %s" % (e, v)
            # pdb.post_mortem()
