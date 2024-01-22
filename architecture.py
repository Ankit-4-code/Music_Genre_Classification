'''
This .py file is to check the supported architecture of the OS. For example this app was tested on a x86_64 architecture.
This is inturn used in --platform=linux/amd64 for the docker build command.

'''

import platform

print(platform.architecture())