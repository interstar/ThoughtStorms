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
git clone https://github.com/WardCunningham/Smallest-Federated-Wiki.git sfw

cd sfw/server/express
npm install

# Install CoffeeScript
npm install -g coffee-script

# Install ThoughtStorms if you want this
cd /home/vagrant
git clone git://github.com/interstar/ThoughtStorms.git thoughtstorms


