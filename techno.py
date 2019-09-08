import click
import os
import time
import json
import sys
import subprocess
from tqdm import tqdm, trange
import requests
import wget
from pathlib import Path
from SI1145 import SI1145
import adafruit_bno055
from busio import I2C
from board import SDA, SCL
import gc
import adafruit_bme680
import board

# home_dir = Path.home()
# ROOT_DIR = os.path.join(home_dir, 'azt/techno')
# # print(ROOT_DIR)

from pyfiglet import Figlet

f = Figlet()
azt_welcome = f.renderText('AzatAI')

_Initialized = False
_Installed = False

__author__ = "Yaakov AZAT"
__email__ = "a@azat.ai"
__copyright__ = "Azat Artificial Intelligence, LLP."


# work_path = ROOT_DIR


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

    # with open('./config.json') as json_file:
    #     data = json.load(json_file)
    #     _ROOT_created = data['_ROOT_created']

    # dirName = work_path
    #
    # try:
    #     os.mkdir(dirName)
    #     print("Directory ", dirName, " Created ")
    # except FileExistsError:
    #     print("Directory ", dirName, " already exists")
    #

    # if _ROOT_created == 0:
    #     try:
    #         os.makedirs(work_path)
    #     except OSError:
    #         click.secho("Creation of the directory %s failed!" % work_path, fg='red')
    #         click.secho("You should try: 'sudo techno --init' ", fg='yellow')
    #         ctx.exit()
    #     else:
    #         click.secho("Successfully created the directory %s " % work_path, fg='green')
    #         data['_ROOT_created'] = 1
    #         with open('./config.json', 'w') as outfile:
    #             json.dump(data, outfile)
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
    click.secho('Orientation Driver installed.', fg='green')

    ctx.exit()


def run(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.secho('Start running the AzatAI Techno Console:', fg='green')
    click.secho("AzatAI Techno Console Started!", fg='green')
    click.secho("Please Press Cntrl + Z to stop! \n WARN: Running code too much time may cause hardware problem!",
                fg='yellow')
    while True:
        click.secho('INFO: The default see level pressure is: 1013.25', fg='blue')
        sea_level_pressure = input('Please Enter sea level pressure:')
        if isinstance(sea_level_pressure, float):
            bme680.sea_level_pressure = sea_level_pressure
        elif isinstance(sea_level_pressure, int):
            bme680.sea_level_pressure = sea_level_pressure
        else:
            click.secho('ERROR! You might entered a wrong value for see level pressure!', fg='red')
            ctx.exit()

        i2c = I2C(SCL, SDA)
        orientation_sensor = adafruit_bno055.BNO055(i2c)
        light_sensor = SI1145.SI1145()
        gc.collect()
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
        # change this to match the location's pressure (hPa) at sea level
        bme680.sea_level_pressure = 1013.25
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        click.secho('BME680:', fg='blue')
        print("\nTemperature: %0.1f C" % bme680.temperature)
        print("Gas: %d ohm" % bme680.gas)
        print("Humidity: %0.1f %%" % bme680.humidity)
        print("Pressure: %0.3f hPa" % bme680.pressure)
        print("Altitude = %0.2f meters" % bme680.altitude)
        click.secho('BNO055', fg='blue')
        print(orientation_sensor.temperature)
        print(orientation_sensor.euler)
        print(orientation_sensor.gravity)
        click.secho('SI1145', fg='blue')
        vis = light_sensor.readVisible()
        _IR = light_sensor.readIR()
        _UV = light_sensor.readUV()
        uvindex = _UV / 100.0
        print('Vis:'+str(vis))
        print("IR"+str(_IR))
        print("UV Index"+str(uvindex))
        time.sleep(3)
    ctx.exit()


def start(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('start')
    ctx.exit()


@click.command()
@click.option('-i', '--init', 'init', is_flag=True, callback=init, expose_value=False,
              help='Initialize the environment\nThis should be done only ONCE '
                   'very first time!')
@click.option('-r', '--run', 'run', is_flag=True, callback=run, expose_value=False,
              help='Run installation. This command installs all the dependencies and drivers of the working sensors.')
@click.option('-s', '--start', 'start', is_flag=True, callback=start, expose_value=False,
              help='Start logging the results, press Ctrl + Z/C to stop.')
def cli():
    click.echo(azt_welcome)
    click.echo(
        'Technopark Raspberry IoT Control Interface\nCopyright:2019 Azat Artificial Intelligence\n...Al-Farabi Kazakh '
        'National University...')


if __name__ == '__main__':
    cli()
