import os.path
import os
import sys
import getpass

# If no platform is matched, use the current directory.
confdir = lambda app: ''
username = getpass.getuser()
posix = lambda app: os.path.join(os.path.expanduser("~"),'.config',app)

confdirs = (
        ('linux', posix),
        ('win32', lambda app: os.path.join(r'C:\Users',username,r'AppData\Local',app)),
        ('cygwin', posix),
        ('darwin', lambda app: os.path.join('/Users',username,'Library/Application Support',app))
    )

for platform, directory in confdirs:
    if sys.platform.startswith(platform):
        confdir = directory

def get(app, conf_file, create=False):
    conf_folder = confdir(app)
    if not os.path.isdir(conf_folder):
        os.makedirs(conf_folder)
    conf_file = os.path.join(conf_folder,conf_file)
    if create and not os.path.isfile(conf_file):
        open(conf_file, 'w').close()
    return conf_file
