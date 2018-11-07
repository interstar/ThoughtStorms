import sys
from fsquery import FSQuery
from thoughtstorms.PageStore import WritablePageStore
import re

# NOTE :: this functionality is now built into TSWiki / the PageStore itself. There should be very little reason to use this 
# standalone script except for handling legacy data.

# 
# A quick and dirty script to move the next "[[SendTo]]" item from the LinkBin page to a local linkbin on the appropriate page.
# Items in the linkbin need to have the format
#
# *Added DATE* : 
# [Link text](https://some.url) [[SendTo]] [[PageName]]

def cleanhead(xs) :
    l = xs[0]
    l = l.strip()
    l = l.encode("utf-8")
    return l

def ensure_linkbin(pages,sendpage,tag="{=LinkBin=}") :
    p = pages.get(sendpage,lambda p, e : "can't find", lambda p, e : "Error %s " % e)
    if tag in p :
        return
    p = p + "\n### LinkBin\n\n"+tag
    pages.put(sendpage,p)


if __name__ == '__main__' :

    if len(sys.argv) < 2 : 
        print "Need pages directory as argument"
    else :
        pwd = sys.argv[1]

        pages = WritablePageStore(pwd,"md",lc=True,recent_changes=True)    
        linkbin = pages.get("linkbin",lambda pname, e : "can't find", lambda pname, e : "Error: %s" % e)
        lines = linkbin.split("\n")
        
        new = []
            
        while True :
            if lines==[] :
                break
                
            l = cleanhead(lines)        
            if not ("*Added" in l) :
                new = new + [l]
                lines = lines[1:]
                continue
            
            d = l
            lines = lines[1:]
            l = cleanhead(lines)

            if not ("[[SendTo]]" in l) :
                new = new + [d]
                new = new + [l]
                lines = lines[1:]
                continue
            
            r = re.compile("(.+)\s+\[\[SendTo\]\] \[\[(\S+)\]\]")   
            m = r.search(l)
            if m :
                sendpage = m.group(2).strip()
                sendtxt = "*Originally* " + d + "\n"+m.group(1).strip()
                print sendpage
                print sendtxt

                y = raw_input("send?")
                if y == "y" :
                    ensure_linkbin(pages,sendpage)                
                    pages.append(sendpage,"{=LinkBin=}",sendtxt)
                else :
                    new = new + [d]
                    new = new + [l]
 
            else :
                print "________________________________ NO MATCH"
            lines = lines[1:]
            break

    print "WRITEBACK ====================================================================="
    #new = [x.decode("utf-8") for x in new + lines]
    new = [x for x in new + lines]
    
    newtxt = "\n".join(new)
    newtxt = newtxt.encode("utf-8")

    print newtxt
    y = raw_input("write back?")
    if y == "y" :
        pages.put("LinkBin",newtxt)
    

