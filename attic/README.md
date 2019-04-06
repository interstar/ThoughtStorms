## Attic

These are some old scripts used during the history of ThoughtStorms wiki. None are really relevant today. But are here in case anyone needs them.

##### Smallest Federated Wiki


ThoughtStorms was, for a time, on the [Smallest Federated Wiki](https://github.com/WardCunningham/Smallest-Federated-Wiki). 

**sfw2flat.py** Converts pages from SFW format to flat files for use in ThoughtStorms Wiki (extracts just the current "story" text). 

     python sfw2flat.py PATH-TO/pages-in-sfw-format/* 

Note that this saves files in the local directory where this is run from, but that the script appends .md on the end of the file-names on the assumption that you will be moving pages to Markdown format.


**wikish2md.py** Converts text files that have *Wikish* markup to Markdown. (Wikish was a variant of UseMod wiki format used in an early incarnation of ThoughtStorms wiki, and on SdiDesk).

    python wikish2md.py PATH-TO/pages-in-wikish/* 
    
NB: saves files with *same name* as originals, in the local directory where this is run from. Be careful. DON'T run this in the same directory as the original files.


##### JSON diff

The `php` directory contains a copy of jsondiff.php which can diff two online JSON files. It's included in the Project ThoughtStorms site as a useful way to diff the same page on two different SFW servers.

##### Other Scripts

The `scripts` directory contains Python files (in CGI) format which can be used to quickly paste in a block of multi-paragraph text and generate an SFW formated page from it. You can try it [here](http://project.thoughtstorms.info/paste.html)


