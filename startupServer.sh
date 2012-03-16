#!/bin/bash


cd /home/vagrant
cp sfw/default-data/pages/* /vagrant/temp_conversion/output

mkdir /home/vagrant/sfw/data

ln -s /vagrant/temp_conversion/output sfw/data/pages

ln -s /vagrant/plugins/wikish.coffee sfw/client/plugins/wikish.coffee


cd sfw/client/plugins

coffee -c /home/vagrant/sfw/client/plugins/wikish.coffee

cd /vagrant/temp_conversion
python /vagrant/scripts/importFiles.py origin/*


