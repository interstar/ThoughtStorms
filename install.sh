#!/bin/bash

# This scripts provisions a VirtualBox (setup with Vagrant with the Lucid32 box) 
# with a copy of node.js and Smallest Federated Wiki

echo "Setting up server"

# Install Git
sudo apt-get install -y git-core

# Install Toolchain
sudo apt-get install -y build-essential

# Install screen cos it's useful
sudo apt-get install -y screen --fix-missing

# Install and build Node.js 
git clone https://github.com/joyent/node.git
cd node
git checkout v0.6.12 #Try checking nodejs.org for what the stable version is
./configure

make
sudo make install

# Install Smallest Federated Wiki
cd /home/vagrant
# Warning, now from my fork
#git clone https://github.com/WardCunningham/Smallest-Federated-Wiki.git sfw
git clone git://github.com/interstar/Smallest-Federated-Wiki.git sfw

cd /home/vagrant/sfw/server/express
npm install

# Install CoffeeScript
npm install -g coffee-script

cd /home/vagrant/sfw
sudo git checkout thoughtstorms

cd /home/vagrant/sfw/client/plugins
sudo coffee -c /home/vagrant/sfw/client/plugins/wikish.coffee


# Install ThoughtStorms if you want this
cd /home/vagrant
git clone git://github.com/interstar/ThoughtStorms.git thoughtstorms
    
