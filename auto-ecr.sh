#!/usr/bin/env bash

FILE=~/.aws/credentials
if test -f "$FILE"; then
    rm -f $FILE
fi
cp ./.aws/credentials $FILE

sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker

declare -a ITEMS
ITEMS=($(docker images --format "{{.Repository}}={{.ID}}"))

IMAGES=()
IMAGES+=("--DONE--")
for i in "${ITEMS[@]}"
do
    set -- `echo $i | tr '=' ' '`
    name=$1
    id=$2
    if [[ "$name" != "<none>" ]]
    then
        THENAME=$(echo "$name=$id")
        IMAGES+=($THENAME)
    fi
done

createmenu ()
{
  select option; do # in "$@" is the default
    if [ "$REPLY" -eq "$#" ];
    then
      echo "Exiting..."
      break;
    elif [ 1 -le "$REPLY" ] && [ "$REPLY" -le $(($#-1)) ];
    then
      echo "$REPLY"
      break;
    else
      echo "Incorrect Input: Select a number 1-$#"
    fi
  done
}

createmenu "${IMAGES[@]}"
