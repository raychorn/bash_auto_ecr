import os, sys
import re
import subprocess

import mujson as json

__docker_images__ = ['docker', 'images', '--format', '{{.Repository}}={{.ID}}']

def parse_docker_image_ls(line):
    return line.replace("b'", "").split('=')

def handle_stdin(stdin, callback=None, verbose=False):
    name_to_id = {}
    id_to_name = {}
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
        if (all([len(t.strip()) > 1 for t in item])):
            name_to_id[item[0]] = item[-1]
            id_to_name[item[-1]] = item[0]
    return name_to_id, id_to_name,

if (__name__ == '__main__'):
    result = subprocess.run(__docker_images__, stdout=subprocess.PIPE)
    name_to_id, id_to_name = handle_stdin(result.stdout, callback=parse_docker_image_ls, verbose=False)
    if (1):
        print(len(id_to_name))
        for k,v in id_to_name.items():
            print('{} -> {}'.format(k,v))
    