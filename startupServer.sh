#!/bin/bash

# Ignore this script. It's only useful for me in my current (disorganized) setup

cd /home/vagrant
cp sfw/default-data/pages/* /vagrant/temp_conversion/output

cp -r /home/vagrant/sfw/default-data /home/vagrant/sfw/data

rm -r sfw/data/pages

ln -s /vagrant/temp_conversion/output sfw/data/pages

#ln -s /vagrant/plugins/wikish.coffee sfw/client/plugins/wikish.coffee

#cd sfw/client/plugins
#coffee -c /home/vagrant/sfw/client/plugins/wikish.coffee

#cd /vagrant/temp_conversion
#python /vagrant/scripts/importFiles.py origin/*


