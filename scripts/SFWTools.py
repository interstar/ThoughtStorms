import random
import re
import json


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
        s = re.sub('\s','-',s)
        s = re.sub('\/','--',s)
        s = re.sub('[^A-Za-z0-9-]','',s)
        s = s.lower()
        return s
        

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
    def __init__(self, fName, body="body",paratype="wikish") :

        self.addPage(fName)

        if body == "body" :
            # we're giving it a filename
            with open(fName) as f :
                s = f.read()
                s = s.decode("Latin1","replace")
                # remove \r
                s = s.replace('\r','\n')
                self.parseBody(s) 

        else :
            # we're giving it actual data
            body = body.replace('\r','\n')
            self.parseBody(body,paratype)                

    def addPage(self,fName) :
        """ We can override this in subclasses"""
        self.page = SfwPage(fName)
    

    def parseBody(self,s,paratype="wikish") :
        build = u""
        try :
            for block in (splitter(outlineSplitterFactory(),s)) :                    
                if block :
                    self.page.addPara(self.process(block.strip()),paratype)
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
        return self.page.slug(self.page.title)
            

class SdiDesk2SFW (UseMod2SFW):
    """ Almost like UseMod but has to strip first couple of lines"""

    def addPage(self,fName) :
        fName = fName.split('/')
        fName = "--".join(fName[3:])
        fName = fName.split('.')[0]
        print "X " + fName
        self.page = SfwPage(fName)

    def parseBody(self,s) :
        build = u""
            
        try :
            blocks = (splitter(outlineSplitterFactory(),s))
            name = (blocks.next()).strip()            
            for count in range(4) :
                s = blocks.next()
                s=s.strip()

            for block in blocks :
                block=block.strip()
                if block == "#Network,, 1" :
                    return self.networkPage(blocks)
                
                if block :
                    self.page.addPara(self.process(block.strip()),"wikish")
        except Exception, e:
            print "error %s in %s" % (e, v)
            pdb.post_mortem()

        self.page.removeBlankParas()

    def networkPage(self,blocks) :
        lines = '\n'.join((x.strip() for x in blocks))
        print lines
        parts = lines.split('----')
        nodes = parts[0]
        arcs = parts[1]
        page = {"type":"sdidesknetwork","id":self.page.randomId(), "text":lines}
        net = {}
        dNodes = {}
        id = 0
        for n in (x.strip() for x in nodes.split("\n")) :
            if not n : continue
            ns = n.split(",,")
            node = {"id" : id, "label":ns[0], "x":int(ns[2]), "y":int(ns[1]), "desc":""}
            dNodes[id] = node
            id=id+1
        net["nodes"] = dNodes
        lArcs = []
        count = 0
        for arc in arcs.split('\n') :
            if not arc : continue
            a = [x.strip() for x in arc.split(",,")]
            def nodeIdFromLabel(label) :
                for node in dNodes.itervalues() :
                    if node["label"] == label :
                        return node["id"]
                        
            d = {"from":nodeIdFromLabel(a[0]), "to":nodeIdFromLabel(a[1]), "directional":a[2], "label":a[3]}
            lArcs.append(d)
        net["arcs"] = lArcs
        
        self.rescale(net)
        page["net"] = net
        self.page.story.append(page)
        
    def addPara(self,data,type="paragraph") :
        self.story.append(self.para(data,type))
            

    def rescale(self,network) :
        maxX = -1
        maxY = -1
        x = "x"
        y = "y"
        for point in network["nodes"].itervalues() :
            if point[x] > maxX : maxX = int(point[x])
            if point[y] > maxY : maxY = int(point[y])
        maxX = maxX + 10
        maxY = maxY + 10
        for point in network["nodes"].itervalues() :
            point[x] = scale(point[x],0,maxX,0,400)
            point[y] = scale(point[y],0,maxY,0,600)      

def scale(x,lo1,hi1,lo2,hi2) :
    return int((float(x-lo1)/float(hi1-lo1) * (hi2-lo2)) + lo2)

