#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Gangdae Ju
# Created Date: Aug 10, 2021
# =============================================================================
import os
import shutil
import argparse
import configparser

version = '0.1.1'

vscenv_run_cmd = 'code' # 'code' or 'code-insider' 
vscenv_dir_path = os.path.join(os.path.expanduser('~'), '.vscenv')
vscenv_conf_path = os.path.join(os.path.expanduser('~'), '.vscenvconfig')

def _list(args):
    global vscenv_dir_path
    for i in os.listdir(vscenv_dir_path):
        print(i)
    return 0

def _create(args):
    global vscenv_dir_path

    codeDir = os.path.join(vscenv_dir_path, args.env)
    userdataDir = os.path.join(codeDir, 'userdata')
    extensionsDir = os.path.join(codeDir, 'extensions')
    
    if os.path.exists(codeDir):
        print(f'ERROR: {args.env} is exist..')
        return -1

    try:
        os.makedirs(codeDir)
        os.makedirs(userdataDir)
        os.makedirs(extensionsDir)
        print('DONE : Successfully created..')
    except OSError:
        print('ERROR: Failed to create..')
        return -1
    
    return 0
    
def _delete(args):
    global vscenv_dir_path

    codeDir = os.path.join(vscenv_dir_path, args.env)

    if not os.path.exists(codeDir):
        print(f'ERROR: {args.env} is not found..')
        return -1

    try:
        shutil.rmtree(codeDir)
        print('DONE : Successfully deleted..')
    except OSError:
        print('ERROR: Failed to delete..')
        return -1
    
    return 0

def _run(args):
    global vscenv_dir_path
    global vscenv_run_cmd
    
    codeDir = os.path.join(vscenv_dir_path, args.env)
    userdataDir = os.path.join(codeDir, 'userdata')
    extensionsDir = os.path.join(codeDir, 'extensions')
    
    cmd = vscenv_run_cmd

    if not os.path.exists(codeDir):
        print(f'ERROR: {args.env} is not found..')
        return -1

    if os.path.exists(userdataDir):
        cmd =f'{cmd} --user-data-dir {userdataDir}'

    if os.path.exists(extensionsDir):
        cmd =f'{cmd} --extensions-dir {extensionsDir}'    
    
    try:
        cmd = f'{cmd} {args.path}'
        os.system(cmd)
    except OSError:
        print(f'ERROR: Faild to run {args.env}.')
        return -1

    return 0

def main():
    global vscenv_conf_path
    global vscenv_dir_path
    global vscenv_run_cmd
    
    if not os.path.exists(vscenv_conf_path):
        config_parser = configparser.ConfigParser()
        config_parser.add_section("setting")
        config_parser.set("setting", "vscenv_run", vscenv_run_cmd)
        config_parser.set("setting", "vscenv_dir", vscenv_dir_path)
        with open(vscenv_conf_path, "w") as fp:
            config_parser.write(fp)
    else:
        config_parser = configparser.ConfigParser()
        config_parser.read(vscenv_conf_path)
        vscenv_run_cmd = config_parser['setting']['vscenv_run']
        vscenv_dir_path = config_parser['setting']['vscenv_dir']
        # print(f'run_cmd = {vscenv_run_cmd}')
        # print(f'dir_path = {vscenv_dir_path}')
  
    if not os.path.exists(vscenv_dir_path):
        os.makedirs(vscenv_dir_path)
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--version', action='version', version=f'vscenv v{version}')

    subparsers = arg_parser.add_subparsers()
    cmd_list = subparsers.add_parser('list', aliases=['l'], help='Show list of vscenv environments.')
    cmd_list.set_defaults(func=_list)
    cmd_create = subparsers.add_parser('create', aliases=['c'], help='Create a new vscenv environmtent.')
    cmd_create.add_argument('env')
    cmd_create.set_defaults(func=_create)
    cmd_delete = subparsers.add_parser('delete', aliases=['d'], help='Delete an vscenv environmtent.')
    cmd_delete.add_argument('env')
    cmd_delete.set_defaults(func=_delete)
    cmd_run = subparsers.add_parser('run', aliases=['r'], help='Executes VSCODE using an vscenv environment.')
    cmd_run.add_argument('env')
    cmd_run.add_argument('path')
    cmd_run.set_defaults(func=_run)
    
    args = arg_parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        arg_parser.parse_args(['-h'])

if __name__ == '__main__':
    main()
