
import logging
logger = logging.getLogger(__name__)


import argparse
import os.path


LOG_LEVELS = {  'debug':    logging.DEBUG,
                'info':     logging.INFO,
                'warning':  logging.WARNING,
                'error':    logging.ERROR,
                'critical': logging.CRITICAL}

from .version import __version__


parser = argparse.ArgumentParser(description='Moving files based on conditions.')

parser.add_argument('--version',
                    action='version',
                    version='%(prog)s {0}'.format(__version__))

parser.add_argument('-c', '--configfile',
                    metavar='~/.scissor.conf',
                    default="~/.scissor.conf",
                    help='Path to configuration file')

parser.add_argument('-d', '--dry-run',
                    action='store_true',
                    default=False,
                    dest='dryrun',
                    help='Do dry run without moving files.')

parser.add_argument('--log-level',
                    dest='loglevel',
                    metavar='debug',
                    default="info",
                    help='Log Level: debug, info, warning, error, critical')


parser.add_argument('files',
                    metavar='filename',
                    nargs='+',   
                    help='List of filenames')



def parse(args=None):
    if args is None:
        options = parser.parse_args()
    else:
        options = parser.parse_args(args)
    
    options.configfile=os.path.expanduser(options.configfile)
    
    if not os.path.isfile(options.configfile):
        parser.error("No configuration file found at {0}".format(options.configfile))
        
    if options.loglevel not in LOG_LEVELS.keys():
        parser.error("Log level \"{0}\" unknown".format(options.loglevel))
    logging.basicConfig(level=LOG_LEVELS.get(options.loglevel, logging.NOTSET))
    
    return options