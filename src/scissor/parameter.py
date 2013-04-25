# Copyright (C) 2013 Sven Klomp (mail@klomp.eu)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.


import argparse
import os.path

import logging
logger = logging.getLogger(__name__)

from .version import __version__



LOG_LEVELS = {  'debug':    logging.DEBUG,
                'info':     logging.INFO,
                'warning':  logging.WARNING,
                'error':    logging.ERROR,
                'critical': logging.CRITICAL}


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

parser.add_argument('--no-cutting',
                    action='store_false',
                    default=True,
                    dest='cut',
                    help='Do not cut files.')

parser.add_argument('--no-moving',
                    action='store_false',
                    default=True,
                    dest='move',
                    help='Do not move files.')

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