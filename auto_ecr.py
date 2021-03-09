import os, sys
import re
import subprocess

import mujson as json

__aws_version__ = ['aws', '--version']
__docker_images__ = ['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}={{.ID}}']

__aws_cli_installer__ = ['./scripts/aws-cli-installer.sh']

__aws_cli__ = 'aws-cli/2'

name_to_id = {}
id_to_name = {}

def handle_aws_cli_installer(item):
    print('DEBUG:  handle_aws_cli_installer --> {}'.format(item))
    return True


def install_aws_cli():
    print('Installing aws cli.')
    result = subprocess.run(__aws_cli_installer__, stdout=subprocess.PIPE)
    handle_stdin(result.stdout, callback2=handle_aws_cli_installer, verbose=True)


def handle_aws_version(item):
    try:
        if (item.find(__aws_cli__) == -1):
            return False
        assert item.find(__aws_cli__) > -1, 'Missing {}'.format(__aws_cli__)
    except:
        return False
    return True


def parse_docker_image_ls(line):
    return line.replace("b'", "").split('=')


def handle_docker_item(item):
    if (all([len(t.strip()) > 1 for t in item])):
        name_to_id[item[0]] = item[-1]
        id_to_name[item[-1]] = item[0]


def handle_stdin(stdin, callback=None, verbose=False, callback2=None):
    lines = str(stdin).split('\\n')
    for line in lines:
        if (verbose):
            print(line)
            #print('-'*30)
        if (callable(callback)):
            try:
                __item__ = callback(line)
            except:
                pass
        item = line if (not callable(callback)) else __item__
        if (callable(callback2)):
            try:
                callback2(item)
            except:
                pass


if (__name__ == '__main__'):
    while (1):
        try:
            result = subprocess.run(__aws_version__, stdout=subprocess.PIPE)
            handle_stdin(result.stdout, callback2=handle_aws_version, verbose=False)
            break
        except:
            install_aws_cli()

    result = subprocess.run(__docker_images__, stdout=subprocess.PIPE)
    handle_stdin(result.stdout, callback=parse_docker_image_ls, callback2=handle_docker_item, verbose=False)
    if (1):
        print(len(id_to_name))
        with open('pulls.sh', 'w') as fOut:
            print('#!/usr/bin/env bash\n', file=fOut)
            for k,v in id_to_name.items():
                print('{} -> {}'.format(k,v))
                print('docker pull {}'.format(v), file=fOut)
    