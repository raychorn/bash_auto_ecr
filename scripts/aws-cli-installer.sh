#!/usr/bin/env bash

cd /tmp
mkdir @1
cd @1

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt-get install unzip zip -y
unzip awscliv2.zip
sudo ./aws/install
