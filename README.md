**PLEASE NOTE : Project ThoughtStorms is now deprecated. If you are interested in a Python-based Wiki Engine, it might suit you. But my interest, and ThoughtStorms are moving to a new wiki-engine and project : [CardiganBay](https://github.com/interstar/cardigan-bay)**

#### Overview

Project ThoughtStorms encompases the software used to run [ThoughtStorms Wiki](http://thoughtstorms.info), and various historical conversion scripts and plugins which have been used to port it to different wiki-engines during its history, and some other tools to manage personal and public information with a wiki-like philosophy.

As of 2019, many of these tools are now redundant and continue in the repository for historical continuity. They have now been moved to the Others are currently in use and under active development.






##### Wiki Software

This repository is now mainly focused on the, currently unnamed, wiki-engine used by ThoughtStorms wiki, which is written in Python.

As of April 2019, we've ported it to Python3. There is no longer any guarantee that it will work with Python2.

As of July 2018, we've moved much of the generic functionality to a library, called "thoughtstorms", which is published on 
PyPI : [https://pypi.org/project/thoughtstorms/](https://pypi.org/project/thoughtstorms/).

The code for this library now lives in a separate repository : [On GitHub](https://github.com/interstar/thoughtstorms-libs) and [On GitLab](https://gitlab.com/interstar/thoughtstorms-libs)

The main wiki itself, and associated templates, css etc. lives in the `tswiki` directory. This wiki uses the minimal [Bottle](http://bottlepy.org/docs/dev/) framework.


Other scripts have now been moved to `attic` in the unlikely event that you might be looking for them.


##### Running the Wiki

We are now using [pipenv](https://github.com/pypa/pipenv) which should handle our dependencies. If you don't want to use pipenv you'll need to install the following :
 
    pip install bottle, pyyaml, markdown, thoughtstorms, fsquery
    
Or with pipenv, go to the `tswiki` directory and :

    pipenv install
    pipenv shell
    
Then

	python wiki.py ThoughtStorms w 8000 PATH-TO-PAGES PATH-TO-SERVICE-PAGES assets

Or, with Docker Compose in the `tswiki` directory :

    docker-compose up

(Note that this also tries to use port 8000 for the wiki. If you want to use a different port you'll need to change the `docker-compose-py` file. Also, this expects the pages, service_pages and assets directories to be subdirectories of tswiki. If you want the pages to be stored elsewhere, you'll also have to change the mapping in `docker-compose.py`

What are these wiki.py options?

    wiki.py wikiname typecode port-number path-to-pages path-to-service-pages path-to-assets
    
The `wikiname` is displayed alongside page-names at the top of each page. (Useful if you are running several wikis at once and need to remember which you are looking at)

The `typecode` selects for the type of PageStore (and the permissions it implies). Currently, typecode 'w' makes the wiki writable by any user. Other typecodes are read-only..

`port-number` determines which port the wiki listens on

`path-to-pages` is path to directory where pages are saved

`path-to-service-pages` is path to a directory where extra functionality "services" store their specific data in the form of YAML files.

`path-to-assets` is path to directory where the html template is stored.


