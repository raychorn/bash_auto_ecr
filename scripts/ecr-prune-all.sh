#!/usr/bin/env bash

venv=$(ls ./.venv*/bin/activate)
. $venv

python ./auto_ecr.py --clean-ecr
