from setuptools import setup, find_packages

setup(
    name='techno',
    version='0.0.2',
    packages=find_packages(),
    include_packages_data=True,
    install_requires=[
        'click',
        'pyfiglet',
        'adafruit-circuitpython-bno055',
        'Adafruit-GPIO',
        'tqdm',
        'requests',
        'wget',
        'colorama'
    ],
    entry_points='''
    [console_scripts]
    techno=techno:cli
    ''',
)
