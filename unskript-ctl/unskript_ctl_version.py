import os 

# Version
VERSION = '1.2.0'
if os.environ.get('VERSION'):
    VERSION = os.environ.get('VERSION')

def get_version():
    if 'BUILD_NUMBER' in globals():
        return globals().get('BUILD_NUMBER')
    else:
        return VERSION 

# Author
AUTHOR = 'unSkript Authors'

# PSS DB Schema Version
SCHEMA_VERSION = '1.0.0'
if os.environ.get('SCHEMA_VERSION'):
    SCHEMA_VERSION = os.environ.get('SCHEMA_VERSION')

