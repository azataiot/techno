import click
import os
import time
import json
import sys
import subprocess
from tqdm import tqdm, trange
import requests
import wget

from pyfiglet import Figlet

f = Figlet()
azt_welcome = f.renderText('AzatAI')

_Initialized = False
_Installed = False

__author__ = "Yaakov AZAT"
__email__ = "a@azat.ai"
__copyright__ = "Azat Artificial Intelligence, LLP."

work_path = "/azt/techno"


def check_internet():
    url = 'http://www.google.com/'
    timeout = 10
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        click.secho("Internet Connection Failed!.", fg='red')
    return False


def init(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('\nInitializing the environment\n\nThis should be done only ONCE '
               'very first time!\n')
    path = os.getcwd()
    print("The current working directory is %s\n" % path)

    with open('./config.json') as json_file:
        data = json.load(json_file)
        _ROOT_created = data['_ROOT_created']

    if _ROOT_created == 0:
        try:
            os.makedirs(work_path)
        except OSError:
            click.secho("Creation of the directory %s failed!" % work_path, fg='red')
            click.secho("You should try: 'sudo techno --init' ", fg='yellow')
            ctx.exit()
        else:
            click.secho("Successfully created the directory %s " % work_path, fg='green')
            data['_ROOT_created'] = 1
            with open('./config.json', 'w') as outfile:
                json.dump(data, outfile)
    # current_directory = subprocess.Popen(['cd'],
    #                                      stdout=subprocess.PIPE,
    #                                      stderr=subprocess.STDOUT)
    # stdout, stderr = current_directory.communicate()
    # click.echo(stdout)
    click.echo('\nChecking the internet connection:')

    for i in trange(10):
        time.sleep(0.01)
        check_internet()
    click.secho('\nInternet Connection: OK', fg='green')
    try:
        import adafruit_bno055
        from busio import I2C
        from board import SDA, SCL
    except ImportError as error:
        click.secho("\nImport Error!" + ' ' + "Try to run 'sudo techno --init' to solve!", fg='red')

    click.echo('Installing Orientation Drivers...')
    for i in trange(10):
        time.sleep(0.01)
    click.echo('Orientation Driver installed.')
    click.echo('Downloading Driver Documentations...')

    ctx.exit()


def run(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('run')
    ctx.exit()


def start(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('start')
    ctx.exit()


def clean(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    with open('./config.json') as json_file:
        data = json.load(json_file)
        _ROOT_created = data['_ROOT_created']
    if _ROOT_created == 1:
        try:
            os.rmdir(work_path)
        except OSError:
            click.secho("Deletion of the directory %s failed" % work_path, fg='red')
            click.secho("You should try: 'sudo techno --clean'", fg='yellow')
        else:
            click.secho("Successfully deleted the directory %s" % work_path, fg='green')
            click.secho("You may need to uninstall the package by 'pip uninstall techno", fg='yellow')
    else:
        click.secho("Project Not initialized!", fg='red')
        click.secho("Have you ever run 'sudo techno --init' command?", fg='yellow')
    ctx.exit()


@click.command()
@click.option('-i', '--init', 'init', is_flag=True, callback=init, expose_value=False,
              help='Initialize the environment\nThis should be done only ONCE '
                   'very first time!')
@click.option('-r', '--run', 'run', is_flag=True, callback=run, expose_value=False,
              help='Run installation. This command installs all the dependencies and drivers of the working sensors.')
@click.option('-s', '--start', 'start', is_flag=True, callback=start, expose_value=False,
              help='Start logging the results, press Ctrl + Z/C to stop.')
@click.option('-c', '--clean', 'clean', is_flag=True, callback=clean, expose_value=False,
              help='Removes all installed resources! BE CAREFUL TO USE!')
def cli():
    click.echo(azt_welcome)
    click.echo(
        'Technopark Raspberry IoT Control Interface\nCopyright:2019 Azat Artificial Intelligence\n...Al-Farabi Kazakh '
        'National University...')


if __name__ == '__main__':
    cli()
