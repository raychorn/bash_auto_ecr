#!/usr/bin/env bash

version=3.9
VENV=.venv
REQS=./requirements.txt

py1=$(whereis python | grep $version)

myid=$(id -u)

sudoprefix=
if (( $EUID != 0 )); then
    sudoprefix="sudo"
else
    sudoprefix=""
fi

if [ -z "$py1" ]
then
    echo "\$py1 is empty"
    $sudoprefix apt update -y
    $sudoprefix apt install software-properties-common -y
    $sudoprefix echo -ne '\n' | add-apt-repository ppa:deadsnakes/ppa
    $sudoprefix apt install python3.9 -y
fi

py1=$(whereis python | grep 3.9)

if [ -z "$py1" ]
then
    echo ""
else
    echo "Python v$version has been installed."
    py39=$(which python3.9)
    echo "py39 -> $py39"
    $sudoprefix apt-get install python3-pip -y
    pypip3=$(which pip3)
    echo "pypip3 -> $pypip3"
    $pypip3 --version
    $pypip3 install virtualenv
    $pypip3 list
    v=$($py39 -c 'import sys; i=sys.version_info; print("{}{}{}".format(i.major,i.minor,i.micro))')
    echo "Use this -> $py39 --> $v"
    VENV=$VENV$v
    echo "VENV -> $VENV"
    if [[ -d $VENV ]]
    then
        rm -R -f $VENV
    fi
    if [[ ! -d $VENV ]]
    then
        virtualenv --python $py39 -v $VENV
    fi
    if [[ -d $VENV ]]
    then
        . ./$VENV/bin/activate
        pip install --upgrade pip

        if [[ -f $REQS ]]
        then
            pip install -r $REQS
        fi

    fi
fi

venv=$(ls ./.venv*/bin/activate)

if [[ -f $venv ]]
then
    . $venv
else
    echo "Cannot find $venv, please run this command in the correct directory."
    exit
fi

python ./auto_ecr.py --push-ecr
