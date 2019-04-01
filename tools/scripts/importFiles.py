from SFWTools import UseMod2SFW, SdiDesk2SFW
import sys
                
if __name__ == '__main__' :
    # Use like this : 
    # python importFiles.py page1 page2 page3 etc.
    # where page1 page2 page3 are plain-text files exported from your wiki
    # NOTE: you must have an "output" subdirectory of the directory where you run 
    # this script, as that's where it will write output 
   
    print sys.argv
    for v in sys.argv[1:] :
        try :
            #conv = UseMod2SFW(v)            
            conv = SdiDesk2SFW(v)
            x = u"%s" % conv
            f = open('output/%s'%(conv.makeFileName()),'w')
            f.write(x)
            f.close()
        except Exception, e:
            print "error %s in %s" % (e, v)
            import pdb
            pdb.post_mortem()
