Project ThoughtStorms encompases the software used to run [ThoughtStorms Wiki](http://thoughtstorms.info), various conversion scripts and plugins which have been used to port it to different wiki-engines during its history, and some other tools to manage personal and public information with a wiki-like philosophy.

As of 2017, some of these tools are now redundant and continue in the repository for historical continuity. Others are currently in use and under active development.

#### Overview

##### Wiki Software

The new, currently unnamed wiki-engine, is written in Python and lives in a the `python` subdirectory of the Project ThoughtStorms repository.

It is, in turn divided into,

 * `python/thoughtstorms` (the libraries used by Project ThoughtStorms)
 * `python/servers` (a wiki server, written using the minimal [Bottle](http://bottlepy.org/docs/dev/) framework, and associated templates and css.
 * `python/conversion` (conversion scripts)
 
The current philosphy is that all the useful intelligence ie. classes that understand different formats, and which manage storage of pages etc. are in the `thoughtstorms` subdirectory. The `servers` subdir contains only a minimal UI logic + templates. `conversions` are batch conversion scripts. Both `servers` and `conversions` reference the intelligence int the thoughtstorms directory.


##### Running the Wiki

	cd PATH-TO/project-thoughtstorms/ThoughtStorms/python/servers

Once in this directory, you need to make sure there's a symbolic link to the `thoughtstorms` directory that contains the libraries. For example, in Linux, type

    ln -s ../thoughtstorms thoughtstorms

This only needs to be done once. Now we're in the right directory, and have the symbolic link, you can type :
	
	python wiki.py ThoughtStorms w 8090 PATH-TO-PAGES PATH-TO/ThoughtStorms/python/servers/assets

What are these wiki.py options?

    wiki.py wikiname typecode port-number path-to-pages path-to-assets
    
The `wikiname` is displayed alongside page-names at the top of each page. (Useful if you are running several wikis at once and need to remember which you are looking at)

The `typecode` selects for the type of PageStore (and the permissions it implies). Currently, typecode 'w' makes the wiki writable by any user. Other typecodes are read-only..

`port-number` determines which port the wiki listens on

`path-to-pages` is path to directory where pages are saved

`path-to-assets` is path to directory where the html template is stored.

##### Conversions

Use the conversion scripts in the `conversion` directory eg.

**sfw2flat.py** Converts SFW files to flat files (extracts just the current "story" text). 

    PATH-TO/project-thoughtstorms/ThoughtStorms/python/conversion/sfw2flat.py PATH-TO/pages-in-sfw-format/* 

Note that this saves files in the local directory where this is run from, but that the script appends .md on the end of the file-names on the assumption that you will be moving pages to Markdown format.


**wikish2md.py** Converts text files that have *Wikish* markup to Markdown. 

    PATH-TO/project-thoughtstorms/ThoughtStorms/python/conversion/wikish2md.py PATH-TO/pages-in-wikish/* 
    
NB: saves files with *same name* as originals, in the local directory where this is run from. Be careful. DON'T run this in the same directory as the original files.



##### JSON diff

The `php` directory contains a copy of jsondiff.php which can diff two online JSON files. It's included in the Project ThoughtStorms site as a useful way to diff the same page on two different SFW servers.

##### Other Scripts

The `scripts` directory contains Python files (in CGI) format which can be used to quickly paste in a block of multi-paragraph text and generate an SFW formated page from it. You can try it [here](http://project.thoughtstorms.info/paste.html)


