## Project ThoughtStorms

Project ThoughtStorms is an umbrella to pull together and refresh a number of things I've worked on over the last 10 or so years. It's now focussed on Ward Cunningham's Smallest Federated Wiki ( https://github.com/WardCunningham/Smallest-Federated-Wiki ) which looks increasingly exciting as the solution to problems that I've had; some of which I didn't even recognise until I saw SFW.

### My Motivation

* I want to update and refresh my personal wiki, ThoughtStorms. This has now been ported to SFW ( http://thoughtstorms.info/ )

* I want to have a wiki with some of the features I prototyped in SdiDesk, a personal wiki-like notebook I wrote for Windows back in the mid-noughties. ( http://code.google.com/p/sdidesk/ )

* I'm buried under piles of paper notebooks where I scribble my ideas. I need a personal wiki to copy those ideas into so I can throw the notebooks into the recycling.

* I have a couple of other services that would make more sense as features embeddable in wiki / dashboard like things.


### Why Smallest Federated Wiki?

* SFW separates into minimal back-end server and a rich client running in the browser. That means I can host personal wikis on my local machine and public copies in the cloud, while the client can run on desktop and mobile devices.

* The client and one implementation of the server are written in CoffeeScript. A language I'm using and liking a lot.

* SFW supports different content-types which can have their own rendering and editing interfaces. And you can extend it with plugins that add new types. That's something I need in order to reproduce the things I did in SdiDesk and for some further projects which have never been released.

* The drag-and-drop refactoring looks like it will be very useful to clean-up and reorganise ThoughtStorms.

* The emphasis on making "federation" easy solves dilemmas like : I'd like to keep some personal information privately in my local wiki but also use a public wiki as a publishing medium. In a sense it seems that SFW is bringing git-like distributed thinking to wiki

* Federation helps resolve the tension between running my own wiki and contributing to a group production. 

* It further resolves similar questions about throwing everything into one wiki or making special-purpose wikis around particular topics.


### What's Here?

* The beginnings of a script to convert pages from flat text files (I've exported mine from UseMod) into SFW's json format

* A Vagrantfile and install.sh script that lets me set up SFW (the node.js / CoffeeScript server) in a Vagrant / VirtualBox on my local machine

* The plugin type for "Wikish", the UseMod derived markup language I use in SdiDesk, has now moved to https://github.com/interstar/wiki-plugin-wikish


### A (Rough) Road Map

* Make sure Wikish covers the most important parts of the UseMod / SdiDesk markup language

* More plugins for the other interesting bits of SdiDesk

* Usable SdiDesk importer

* A "gateway" that can wrap UseMod / OddMuse wikis so that they look like SFW. (They'll be static, but it will be possible to drag paragraphs from them into SFW)

* Me sorting myself out with private and public servers.

* Some other half-baked projects, now imported into SFW

