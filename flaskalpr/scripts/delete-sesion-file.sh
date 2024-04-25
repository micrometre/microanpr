#!/bin/bash
files_path="/home/vagrant/flaskalpr/flaskalpr/static/"
ls $files_path
sudo rm -rf $files_path/alprd1_images/
sudo rm -rf $files_path/camera1_images/
sudo mkdir $files_path/camera1_images/
sudo mkdir $files_path/alprd1_images
