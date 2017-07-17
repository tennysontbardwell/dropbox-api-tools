#!/usr/bin/env bash
apt-get update
apt-get install -y emacs python3 python3-pip

pip3 install -r requirements.txt
