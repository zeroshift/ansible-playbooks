#!/usr/bin/env python

import argparse
import logging


def _get_args():
    """Get arguments and options."""
    parser = argparse.ArgumentParser(description='CHANGEME',
                                     prog='CHANGEME.py')

    parser.add_argument('-l', '--log-level',
                        dest='log', action='store', default="warning",
                        metavar="LOG LEVEL",
                        help='Set the log level. (Default: %(default)s)')
    parser.add_argument('--log-file',
                        dest='log_file', action='store', default=None,
                        metavar="LOG_FILE",
                        help='Set the log file.')

    args = parser.parse_args()
    return args


def main():

    args = _get_args()
    # Setup Logging
    numeric_log_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    logging.basicConfig(level=numeric_log_level,
                        format='[%(asctime)s %(levelname)s] ' +
                        '[CHANGEME] %(message)s',
                        datefmt='%Y%m%d %H:%M:%S',
                        filename=args.log_file)

    logging.info("Starting up...")
    # Start

    # End
    logging.info("Shutting down ...")

if __name__ == '__main__':
    main()
