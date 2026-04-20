"""
Command-line interface for SMC360.
"""

import argparse
from smc360 import SocialMediaConnector, __version__
from smc360.explorer.app import explorer
        
def main(argv=None):
    parser = argparse.ArgumentParser(description='Social media parser for analyzing and exploring social media data.')
    parser.add_argument('-c', '--config', type=str, metavar="path/to/config", help='path to system configuration file')
    parser.add_argument('-v', '--version', action='version', version=f'smc360 version {__version__}')
    parser.add_argument('-e', '--explorer', action='store_true', help='start explorer')
    args = parser.parse_args(argv)

    if not any(vars(args).values()):
        print('''      
         _______  __   __  _______  _______  ___      _______ 
        |       ||  |_|  ||       ||       ||   |    |  _    |
        |  _____||       ||      _||___    ||   |___ | | |   |
        | |_____ |       ||     |   ___|   ||    _  || | |   |
        |_____  ||       ||     |  |___    ||   | | || |_|   |
         _____| || ||_|| ||     |_  ___|   ||   |_| ||       |
        |_______||_|   |_||_______||_______||_______||_______| 

        This program extracts data from social media platforms and stores 
        parsed data in a database and raw response in object storage. The 
        program will use the configuration data to connect to the social 
        media platform, database, and object storage service. It will then 
        load additional configuration data from the object storage service, 
        parse the social media data, and store it in the database.

        The program supports the following services:
        - Platform: YouTube(Youtube Data API), Instagram(Basic Display API)
        - Database: PostgreSQL, Snowflake
        - Object Storage: s3

        Run: `smc360 -h` to get started.
        ''')
        return

    if args.config is not None:
        SocialMediaConnector(args.config).run()
    if args.explorer:
        explorer()
