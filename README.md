Project ThoughtStorms encompases the software used to run [ThoughtStorms Wiki](http://thoughtstorms.info), various conversion scripts and plugins which have been used to port it to different wiki-engines during its history, and some other tools to manage personal and public information with a wiki-like philosophy.

As of 2018, some of these tools are now redundant and continue in the repository for historical continuity. Others are currently in use and under active development.


#### Overview

##### Wiki Software

The new, currently unnamed wiki-engine, is written in Python.

As of July 2018, we've moved much of the functionality to a library, called "thoughtstorms", which is published on PyPI : [https://pypi.org/project/thoughtstorms/](https://pypi.org/project/thoughtstorms/)

The code for this libray lives in the `python/thoughtstorms` directory.

The main wiki itself, and associated templates, css etc. lives in the `python/servers` directory. This wiki uses the minimal [Bottle](http://bottlepy.org/docs/dev/) framework.

Some other conversion scripts are in `python/conversion`.



##### Running the Wiki

We are now using [pipenv](https://github.com/pypa/pipenv) which should handle our dependencies. If you don't want to use pipenv you'll need to install the following :
 
    pip install bottle, pyyaml, markdown, thoughtstorms
    
Or with pipenv, go to the `python/servers` directory and :

	cd PATH-TO/THIS-REPO/python/servers	
    pipenv install
    pipenv shell
    
Then

	cd PATH-TO/THIS-REPO/python/servers	
	python wiki.py ThoughtStorms w 8090 PATH-TO-PAGES PATH-TO-SERVICE-PAGES PATH-TO/THIS-REPO/python/servers/assets

What are these wiki.py options?

    wiki.py wikiname typecode port-number path-to-pages path-to-service-pages path-to-assets
    
The `wikiname` is displayed alongside page-names at the top of each page. (Useful if you are running several wikis at once and need to remember which you are looking at)

The `typecode` selects for the type of PageStore (and the permissions it implies). Currently, typecode 'w' makes the wiki writable by any user. Other typecodes are read-only..

`port-number` determines which port the wiki listens on

`path-to-pages` is path to directory where pages are saved

`path-to-service-pages` is path to a directory where extra functionality "services" store their specific data in the form of YAML files.

`path-to-assets` is path to directory where the html template is stored.

##### Conversions

Use the conversion scripts in the `conversion` directory eg.


ThoughtStorms was, for a time, on the [Smallest Federated Wiki](https://github.com/WardCunningham/Smallest-Federated-Wiki). 

**sfw2flat.py** Converts pages from SFW format to flat files for use in ThoughtStorms Wiki (extracts just the current "story" text). 

    PATH-TO/THIS-REPO/python/conversion/sfw2flat.py PATH-TO/pages-in-sfw-format/* 

Note that this saves files in the local directory where this is run from, but that the script appends .md on the end of the file-names on the assumption that you will be moving pages to Markdown format.


**wikish2md.py** Converts text files that have *Wikish* markup to Markdown. (Wikish was a variant of UseMod wiki format used in an early incarnation of ThoughtStorms wiki, and on SdiDesk).

    PATH-TO/THIS-REPO/python/conversion/wikish2md.py PATH-TO/pages-in-wikish/* 
    
NB: saves files with *same name* as originals, in the local directory where this is run from. Be careful. DON'T run this in the same directory as the original files.



##### JSON diff

The `php` directory contains a copy of jsondiff.php which can diff two online JSON files. It's included in the Project ThoughtStorms site as a useful way to diff the same page on two different SFW servers.

##### Other Scripts

The `scripts` directory contains Python files (in CGI) format which can be used to quickly paste in a block of multi-paragraph text and generate an SFW formated page from it. You can try it [here](http://project.thoughtstorms.info/paste.html)


