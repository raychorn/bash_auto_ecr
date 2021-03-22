#!/usr/bin/env bash

cd /tmp
mkdir @1
cd @1

cpu_arch=$(uname -m)

curl "https://awscli.amazonaws.com/awscli-exe-linux-$cpu_arch.zip" -o "awscliv2.zip"
sudo apt-get install unzip zip -y
unzip awscliv2.zip
sudo ./aws/install --update
