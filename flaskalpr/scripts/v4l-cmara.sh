#!/bin/bash
sudo apt install v4l2loopback-dkms
sudo apt install v4l-utils
sudo apt install ffmpeg
sudo modprobe v4l2loopback
#sudo modprobe v4l2loopback devices=2