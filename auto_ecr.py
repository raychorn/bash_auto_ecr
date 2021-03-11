import os, sys
import re
import shutil
import subprocess
import traceback

import mujson as json

__aws_creds_dest__ = '~/.aws/credentials'
__aws_creds_src__ = './.aws/credentials'

__aws_config_dest__ = '~/.aws/config'
__aws_config_src__ = './.aws/config'

__cat_aws_creds__ = ['cat', __aws_creds_dest__]
__cat_aws_config__ = ['cat', __aws_config_dest__]

__aws_version__ = ['aws', '--version']
__docker_images__ = ['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}={{.ID}}']

__aws_cli_installer__ = ['./scripts/aws-cli-installer.sh']

__resolve_docker_issues__ = ['./scripts/resolve-docker-issues.sh']

__docker_hello_world__ = ['docker', 'run', 'hello-world']

__aws_docker_login__ = ['aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin http://link-for-your-repository-goes-here']
__aws_docker_login__ = __aws_docker_login__[0].split()

__aws_cli_login__ = ['aws ecr get-login --no-include-email --region us-east-2']
__aws_cli_login__ = __aws_cli_login__[0].split()

__aws_cli_ecr_describe_repos__ = ['aws', 'ecr', 'describe-repositories']

__aws_cli_ecr_create_repo__ = ['aws', 'ecr', 'create-repository', '--repository-name']

__aws_cli__ = 'aws-cli/2.'
__hello_from_docker__ = 'Hello from Docker!'
__no_such_file_or_directory__ = 'No such file or directory'

__docker_pulls__ = './script/pulls.sh'

name_to_id = {}
id_to_name = {}

response_vectors = {}

current_aws_creds = {}

response_content = []

ignoring_image_names = ["hello-world"]

def handle_resolve_docker_issues(item):
    print('DEBUG:  handle_resolve_docker_issues --> {}'.format(item))
    return True


def handle_docker_hello(item):
    try:
        __is__ = item.find(__hello_from_docker__)
        if (__is__ == -1):
            return False
        assert (__is__ > -1), 'Missing {}'.format(__hello_from_docker__)
        print('{}'.format(item))
    except:
        return False
    return True


def handle_aws_cli_installer(item):
    print('DEBUG:  handle_aws_cli_installer --> {}'.format(item))
    return True


def install_aws_cli():
    print('Installing aws cli.')
    result = subprocess.run(__aws_cli_installer__, stdout=subprocess.PIPE)
    handle_stdin(result.stdout, callback2=handle_aws_cli_installer, verbose=True)


def resolve_docker_issues():
    print('Resolving docker issues.')
    result = subprocess.run(__resolve_docker_issues__, stdout=subprocess.PIPE)
    handle_stdin(result.stdout, callback2=handle_resolve_docker_issues, verbose=True)



def handle_aws_version(item):
    __vector__ = response_vectors.get(__aws_cli__, None)
    if (__vector__ is None):
        try:
            __is__ = item.find(__aws_cli__)
            if (__is__ == -1):
                return False
            assert (__is__ > -1), 'Missing {}'.format(__aws_cli__)
            print('{}'.format(item))
            response_vectors[__aws_cli__] = __is__
        except:
            return False
    return True

def resolve_missing_file_dest(src_name, dest_name):
    from pathlib import Path

    if (dest_name.find('~') > -1):
        dest_name = os.path.expanduser(dest_name)
    if (src_name.find('~') > -1):
        src_name = os.path.expanduser(src_name)
    if (not os.path.exists(dest_name)):
        assert os.path.exists(src_name) and os.path.isfile(src_name), 'Missing {}. Please resolve.'.format(src_name)
        Path(dest_name).touch()
        shutil.copyfile(src_name, dest_name)
        assert os.path.exists(dest_name) and os.path.isfile(dest_name), 'Missing {}. Please resolve by ensuring {} is available.'.format(dest_name, src_name)

def handle_cat_aws_creds(item):
    resolve_missing_file_dest(__aws_creds_src__, __aws_creds_dest__)
    return os.path.exists(os.path.expanduser(__aws_creds_dest__)) and os.path.isfile(os.path.expanduser(__aws_creds_dest__))

def handle_cat_aws_config(item):
    resolve_missing_file_dest(__aws_config_src__, __aws_config_dest__)
    return os.path.exists(os.path.expanduser(__aws_config_dest__)) and os.path.isfile(os.path.expanduser(__aws_config_dest__))



def handle_aws_login(item):
    return None


def handle_ecr_describe_repos(item):
    return None


def parse_docker_image_ls(line):
    return line.replace("b'", "").split('=')


def handle_docker_item(item):
    if (all([len(t.strip()) > 1 for t in item])):
        name_to_id[item[0]] = item[-1]
        id_to_name[item[-1]] = item[0]


def json_loads(content):
    content = content.replace("b\'", "").replace("\'", "")
    return json.loads(content)


def handle_stdin(stdin, callback=None, verbose=False, callback2=None, is_json=False):
    response_content = []
    lines = str(stdin).split('\\n')
    for line in lines:
        resp = None
        if (verbose):
            print(line)
        if (callable(callback)):
            try:
                __item__ = callback(line)
            except Exception as ex:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                del exc_info
        item = line if (not callable(callback)) else __item__
        if (callable(callback2)):
            try:
                resp = callback2(item)
                if (resp):
                    break
            except Exception as ex:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                del exc_info
        response_content.append(item)
    __content = ''
    if (is_json):
        __content = ''.join(response_content)
        data = json_loads(__content)
    return resp if (resp is not None) else data if (is_json) else __content


if (__name__ == '__main__'):
    print('Checking for aws creds.')
    result = subprocess.run(__cat_aws_creds__, stdout=subprocess.PIPE)
    resp = handle_stdin(result.stdout, callback2=handle_cat_aws_creds, verbose=False)
    assert resp == True, 'Cannot verify the aws creds.  Please resolve.'

    print('Checking for aws config.')
    result = subprocess.run(__cat_aws_config__, stdout=subprocess.PIPE)
    resp = handle_stdin(result.stdout, callback2=handle_cat_aws_config, verbose=False)
    assert resp == True, 'Cannot verify the aws config.  Please resolve.'

    if (0):
        print('Using the aws creds.')
        result = subprocess.run(__aws_cli_login__, stdout=subprocess.PIPE)
        resp = handle_stdin(result.stdout, callback2=handle_aws_login, verbose=False)
        assert resp == True, 'Cannot login using the aws creds.  Please resolve.'

    print('Checking for aws cli version 2.')
    resp = None
    while (1):
        try:
            result = subprocess.run(__aws_version__, stdout=subprocess.PIPE)
            resp = handle_stdin(result.stdout, callback2=handle_aws_version, verbose=False)
            break
        except:
            install_aws_cli()
        finally:
            if (not resp):
                print('Warning: Cannot resolve aws cli issues automatically. Please run the script manually. See the "script" directory.')
                break

    print('Checking for docker.')
    resp = None
    while (1):
        try:
            result = subprocess.run(__docker_hello_world__, stdout=subprocess.PIPE)
            resp = handle_stdin(result.stdout, callback2=handle_docker_hello, verbose=False)
            break
        except:
            resolve_docker_issues()
        finally:
            if (not resp):
                print('Warning: Cannot resolve docker issues automatically. Please run the script manually. See the "script" directory.')
                break

    result = subprocess.run(__docker_images__, stdout=subprocess.PIPE)
    resp = handle_stdin(result.stdout, callback=parse_docker_image_ls, callback2=handle_docker_item, verbose=False)
    if (0):
        print(len(id_to_name))
        with open(__docker_pulls__, 'w') as fOut:
            print('#!/usr/bin/env bash\n', file=fOut)
            for k,v in id_to_name.items():
                print('{} -> {}'.format(k,v))
                print('docker pull {}'.format(v), file=fOut)
                
    assert len(id_to_name) > 0, 'There are no docker images to handle.  Please resolve.'
    print('There are {} docker images.'.format(len(id_to_name)))
    
    print('{}'.format(__aws_cli_ecr_describe_repos__))
    result = subprocess.run(__aws_cli_ecr_describe_repos__, stdout=subprocess.PIPE)
    resp = handle_stdin(result.stdout, callback2=None, verbose=False, is_json=True)
    assert 'repositories' in resp.keys(), 'Cannot "{}".  Please resolve.'.format(__aws_cli_ecr_describe_repos__)
    
    print(json.dumps(resp, indent=3))
    
    create_the_repos = []
    the_repositories = resp.get('repositories', [])
    for image_id,image_name in id_to_name.items():
        __is__ = False
        possible_repo_name = image_name.split(':')[0]
        if (possible_repo_name not in ignoring_image_names):
            for repo in the_repositories:
                if (possible_repo_name == repo.get('repositoryName')):
                    __is__ = True
                    continue
            if (not __is__):
                create_the_repos.append(possible_repo_name)
                
    print(json.dumps({'create_the_repos': create_the_repos}, indent=3))
    
    for name in create_the_repos:
        print('Create ECR repo "{}"'.format(name))
        cmd = __aws_cli_ecr_create_repo__
        cmd.append(name)
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        resp = handle_stdin(result.stdout, callback2=None, verbose=False, is_json=True)
        assert 'repositories' in resp.keys(), 'Cannot "{}".  Please resolve.'.format(' '.join(cmd))
    