import os 

# Version
VERSION = '1.2.0'
if os.environ.get('VERSION'):
    VERSION = os.environ.get('VERSION')

# Author
AUTHOR = 'unSkript Authors'

# Build Number
BUILD_NUMBER = '1.2.0'
if os.environ.get('BUILD_NUMBER'):
    BUILD_NUMBER = os.environ.get('BUILD_NUMBER')

# PSS DB Schema Version
SCHEMA_VERSION = '1.0.0'
if os.environ.get('SCHEMA_VERSION'):
    SCHEMA_VERSION = os.environ.get('SCHEMA_VERSION')