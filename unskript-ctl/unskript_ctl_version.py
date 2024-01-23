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
