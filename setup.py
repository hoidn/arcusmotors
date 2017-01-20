from setuptools import setup, find_packages
import os

setup(name = 'arcusmotors',
    packages = find_packages('.'),
    package_dir = {'arcusmotors': 'arcusmotors'},
    package_data = {'arcusmotors': ['Performax_Linux_Driver_104/*']},
#    scripts = [
#        'bin/oacapture'
#        ],
    #install_requires = ['paramiko', 'numpy', 'matplotlib', 'mpld3', 'plotly', 'humanfriendly', 'multiprocess'],
    zip_safe = False)