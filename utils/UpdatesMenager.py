import os
import shutil
import datetime
import random
import string
from git import Repo
import requests


"""
The UpdatesManager script has been customized for this application.
The regular version can be found on GitHub: https://github.com/Metor7/Updates-menager

It is recommended to clear the tmp folder every 4-6 updates - information in logs.

Name: Updates Menager
Author: Metor
Version: 1.1.0 - Version individually adapted for use by the SyncLore application.
Description: Updates Manager is a Python script that automates application updates using a GitHub repository as a file server.
Publication date: 06.21.2023
Last update date: -
"""

def _get_latest_version(version_file: str = None,
                        console = None,
                        print_info: bool = True):
    version_file = version_file

    response = requests.get(version_file)
    content = response.text

    lines = content.strip().split('\n')
    first_line = lines[0] if lines else ''

    #print(f'UpdatesMenager: App version on server: {first_line}.')
    if print_info:
        console.log('INFO', f'UpdatesMenager: App version on server: {first_line}')
    else:
        print('')

    return first_line

def update_files(repo_url: str = None,
                destination_folder: str = 'App',
                console = None):
    repo_url = repo_url
    destination_folder = destination_folder

    current_date = datetime.datetime.now().strftime('%m-%d-%Y')
    random_update_num = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    temp_folder = f'tmp/{current_date}_{random_update_num}'
    #print(f'UpdatesMenager: Created {temp_folder} temp folder for clone.')
    console.log('INFO', f'UpdatesMenager: Created {temp_folder} temp folder for clone.')

    Repo.clone_from(repo_url, temp_folder)

    for root, dirs, files in os.walk(temp_folder):
        for name in files:
            src_file = os.path.join(root, name)
            dest_file = os.path.join(destination_folder, os.path.relpath(src_file, temp_folder))
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src_file, dest_file)

    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)

    #print('UpdatesMenager: The cloning of repository was successful.')
    console.log('INFO', 'UpdatesMenager: The cloning of repository was successful.')


def _check_clear_tmp_folder_need(console = None):
    subfolders = next(os.walk('tmp'))[1]

    if len(subfolders) > 5:
        console.log('WARNING', 'UpdatesMenager: Need to clear tmp folder.')
        return True
    else:   
        return False

def _get_installed_version(installed_version_file: str = None,
                           console = None):
    installed_version_file = installed_version_file

    with open(installed_version_file, 'r') as file:
        installed_version = file.readline().strip()

    #print(f'UpdatesMenager: Your installed app version: {installed_version}.')
    console.log('INFO', f'UpdatesMenager: Your installed app version: {installed_version}.')

    return installed_version

def _check_update_need(installed_app_version: str = None,
                       version_path: str = None,
                       console = None):
    latest_app_ver = _get_latest_version(version_file=version_path, console=console)
    installed_app_verson = installed_app_version

    if latest_app_ver == installed_app_verson:
        #print('UpdatesMenager: Update is needed[true/false]: False.')
        console.log('INFO', 'UpdatesMenager: Update is needed[true/false]: False.')
        return False
    if latest_app_ver < installed_app_verson:
        #print('UpdatesMenager: Update is needed[true/false]: False.')
        console.log('INFO', 'UpdatesMenager: Update is needed[true/false]: False.')
        return False
    else:
        #print('UpdatesMenager: Update is needed[true/false]: True.')
        console.log('WARNING', 'UpdatesMenager: Update is needed[true/false]: True.')
        return True

def update_app(download_repo_url: str = None,
               destination_folder: str = None,
               installed_app_version_file: str = None,
               server_version_path: str = None,
               console = None):
    download_repo_url = download_repo_url
    destination_folder = destination_folder
    installed_app_version_file = _get_installed_version(installed_app_version_file, console=console)
    server_version_path = server_version_path
    console = console

    update_is_needed = _check_update_need(installed_app_version=installed_app_version_file, version_path=server_version_path, console=console)

    if update_is_needed:
        #print('UpdatesMenager: Updating app...')
        console.log('INFO', 'UpdatesMenager: Updating app...')
        update_files(repo_url=download_repo_url, destination_folder=destination_folder, console=console)

        if _check_clear_tmp_folder_need(console=console):
            #print('Clear tmp folder is needed!')
            console.log('WARNING', 'UpdatesMenager: Clear tmp folder is needed!')
    else:
        #print('UpdatesMenager: The current version is installed.')
        console.log('INFO', 'UpdatesMenager: The current version is installed.')

# Usage (update_files):
#update_files(repo_url='<link to your repository>', destination_folder='<path to destination folder>')

# Usage (update_app):
#update_app(installed_app_version='<installed app version(0.0.0)>', download_repo_url='<link to your repository>', destination_folder='App', version_path='<link to raw with version file>')
#update_app(installed_app_version='1.0.0', download_repo_url='https://github.com/Metor7/DownloadMenagerTests.git', destination_folder='App', version_path='https://raw.githubusercontent.com/Metor7/DownloadMenagerTests/main/VERSION')
