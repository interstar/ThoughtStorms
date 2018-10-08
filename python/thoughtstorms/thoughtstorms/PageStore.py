
from subprocess import check_output, CalledProcessError

import datetime, re, csv

class PageStore :
        
    def __init__(self,pages_dir,extension,lc=False) :
        self.pages_dir = pages_dir
        self.extension = extension
        self.lower_case = lc
        self.init_common()

    def init_common(self) :
        self.work_dir = "%s/.work" % self.pages_dir
        self.old_files_dir = "%s/old_pages" % self.work_dir
        import os
        try:
            os.makedirs(self.old_files_dir)
        except Exception, e :
            print e

            
    def __str__(self) :
        return "(ReadOnly) PageStore with pages at %s" % self.pages_dir
    
    def fName(self,pName) :
        if self.lower_case :
            pName=pName.lower()            
        return "%s/%s.%s" % (self.pages_dir,pName,self.extension)
        
    def old_fName(self,pName) :
        if self.lower_case :
            pName=pName.lower()
        return "%s/%s.%s" % (self.old_files_dir,pName,self.extension)

        
    def get(self,pName,no_file_handler,other_error_handler) :
        file_name = self.fName(pName)
        try :
            with open(file_name) as f :
                return f.read().decode("utf-8")
        except Exception, e :
            if "No such file or directory:" in "%s"%e :
                return no_file_handler(pName,e)
            else :
                return other_error_handler(pName,e)
    
    def get_old(self,pName,no_file_handler,other_error_handler) :
        file_name = self.old_fName(pName)
        try :
            with open(file_name) as f :
                return f.read().decode("utf-8")
        except Exception, e :
            if "No such file or directory:" in "%s"%e :
                return no_file_handler(pName,e)
            else :
                return other_error_handler(pName,e)
    

    def is_writable(self) : return False
    
    def put(self,pName,body) :
        raise Exception("This PageStore doesn't allow writing")
        
    def append(self,pName,marker,extra) :
        raise Exception("This PageStore doesn't allow writing. So also doesn't allow appending")

    def delete(self,pname) :
        raise Exception("This PageStore doesn't allow deleting")
        
    def is_searchable(self) : return True
    
    def file_name_2_page_name(self,fName) :
        print fName
        r = fName.split("/")[-1]
        r = r[:-len(self.extension)-1]
        print r
        return r
            
    def search(self,text) :
        try  :
            res = check_output(["""grep -i "%s" %s/*.%s""" % (text,self.pages_dir,self.extension)], shell=True)
        except CalledProcessError, e :
            if e.returncode == 1 :
                return "No results"
            else :
                raise e
        rs = res.split("\n")
        def f(l) :
            r = self.file_name_2_page_name(l.split(":")[0])            
            return "* [[%s]]" % r
        rs = sorted(set([f(r) for r in rs ]))        
        return "\n".join(rs)

    def all_pages(self) :
        res = check_output(["ls %s/*.%s" % (self.pages_dir,self.extension)],shell=True).split("\n")        
        res = sorted(set([self.file_name_2_page_name(x) for x in res]))
        return res
        
                
class WritablePageStore(PageStore) :

    def __init__(self,pages_dir,extension,recent_changes=False,lc=False) :
        self.pages_dir = pages_dir
        self.extension = extension
        self.lower_case = lc
        self.recent_changes = recent_changes
        self.init_common()
        


    def __str__(self) :
        return "Read/Write PageStore with pages at %s" % self.pages_dir

    def is_writable(self) : return True

    def update_recent_changes(self,pName) :
        r_sqr = re.compile("(\[\[(\S+?)\]\])")
        
        xs = self.get("RecentChanges",lambda pname, e : "", lambda pname, e : "Error %s " % e)
        xs = xs.split("\n")                 
        xs = (["* [[%s]] %s" % (pName,datetime.date.today())] + xs)

        ys = []
        seen = set([])
        for x in xs :
            try :
                pname = r_sqr.finditer(x).next().groups()[1]
                if not pname in seen :
                    seen.add(pname)
                    ys.append(x)
            except Exception, e :
                pass
                
        ys = ys[:50]

        f = open(self.fName("recentchanges"),'w')
        f.write("\n".join(ys))
        f.close()
        
    def save_old(self,pName) :
        try :
            with open(self.fName(pName)) as old_f :
                old_body = old_f.read()
        except Exception, e :
            if "No such file or directory:" in "%s"%e :
                old_body = ""
            else :
                print e
                raise e
        with open(self.old_fName(pName),"w") as old_f :
            old_f.write(old_body)
            
    def recent_changes_name(self) :
        return "%s/recentchanges.csv" % self.work_dir


    def get_recentchanges(self) :
        try :        
            rc = open(self.recent_changes_name())
            return rc.readlines()
        except Exception, e :
            if "No such file or directory:" in "%s"%e :
                return []
            else :
                print e
                raise e

    def new_recent_changes(self,pName) :
        new =  ["%s, %s" % (pName,datetime.date.today())]
        xs = new + self.get_recentchanges()
        seen = set([])
        ys = []
        for x in xs :
            n = x.split(",")[0]
            if not n in seen :
                seen.add(n)
                ys.append(x)
        
        rc = open("%s/recentchanges.csv" % self.work_dir,"w")
        rc.write("\n".join(ys))
        rc.close()


    def put(self,pName,body) :
        self.save_old(pName)
                            
        f = open(self.fName(pName),"w")
        f.write(body)
        f.close()

        if self.recent_changes :            
            self.update_recent_changes(pName)
            self.new_recent_changes(pName)
            
    def append(self,pName,marker,extra) :
        f = open(self.fName(pName)) 
        page = f.read()
        if not marker in page :
            print "Marker %s not found in page %s " % (marker, page)
            return
        lines = page.split("\n")
        before, after = [],[]
        flag = False
        for l in lines : 
            if not flag :                
                if marker in l :
                    flag = True
                before = before + [l]
            else :
                after = after + [l]
        if "\n" in extra :
            extra = extra.split("\n")
        else :
            extra = [extra]
        newpage = before + ["","*Added %s* : " % datetime.date.today()] + extra + [""] + after
        f.close()
        
        self.put(pName,"\n".join(newpage))
        
    def extract_block_by_match(self,pagebody,matchtext) :
        """ Matches the first block separated by newlines that contains match in the page ... and returns a) page without it and b) the block"""
        lines = pagebody.split("\n")
        before, after, found = [],[],""
        while True :
            if lines == [] : break
            else :
                l = lines[0]
                lines = lines[1:]
                if matchtext in l :
                    found = before[-1] + "\n" + l
                    before = "\n".join(before[0:-1])
                    after = "\n".join(lines)
                    break
                else :
                    before = before + [l]
        return before+after,found

    def move_first_linkbin_sendto(self) :
        lb = self.get("LinkBin",lambda pname, e : "Can't find LinkBin " + e, lambda pname, e : "Error: %s %s" % (pname,e) )
        lb, link = self.extract_block_by_match(lb,"[[SendTo]]")
        
        def ensure_linkbin(sendpage,tag="{=LinkBin=}") :
            p = self.get(sendpage,lambda p, e : "can't find", lambda p, e : "Error %s " % e)
            if tag in p :
                return
            p = p + "\n### LinkBin\n\n"+tag
            self.put(sendpage,p)

        print "sending to"
        print link
        
        r = re.compile("(.+)\s+\[\[SendTo\]\]\s+\[\[(\S+)\]\]")   
        m = r.search(link)
        
        if m :
            sendpage = m.group(2).strip()
            dr = re.compile("Added ([0-9-]+)")
            dm = dr.search(link)
            if dm : 
                od = dm.group(1).strip()
            else :
                od = ""
            sendtxt = "*Originally* " + od + "\n\n"+m.group(1).strip()
            print "sendpage : ", sendpage
            print "sendtxt : ", sendtxt

            ensure_linkbin(sendpage)
            self.append(sendpage,"{=LinkBin=}",sendtxt)
            print lb
            self.put("LinkBin",lb.encode("utf-8"))
        
        return lb
       
        
                    
    def delete(self,pname) :
        with open(self.fName(pname)) as f :
            body = """You deleted %s

The following text has now gone from your system. This is your last chance to save it, by copying and recreating the page.
            
            <pre>\n\n %s \n\n</pre>  
            
Go <a href="/view/%s">here to recreate the page</a>. (But don't forget to copy first.""" % (pname, f.read(), pname)            
            res = check_output(["rm %s" % self.fName(pname)], shell=True)
            print res
            return body
