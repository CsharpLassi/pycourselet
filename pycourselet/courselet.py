# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

__author__ = "Lassi"
__copyright__ = "Lassi"
__license__ = "gplv3"

__version__ = "0.1.0"

try:
    from .generator import CourseletGenerator
except ImportError:
    from generator import CourseletGenerator

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        prog='exschoolCourselet',
        description="Generate courselets from directory")
    parser.add_argument(
        "--version",
        action="version",
        version="exschool {ver}".format(ver=__version__))
    parser.add_argument(
        '-n', '--name',
        dest="name",
        help="name",
        type=str,
        default=None,
        metavar="name")
    parser.add_argument(
        dest="courselet_dir",
        help="courselet directory",
        type=str,
        metavar="dir")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="save output to file",
        type=str)
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    if not os.path.isdir(args.courselet_dir):
        _logger.exception(f"'{args.courselet_dir}' is not an directory")
        return 1

    _logger.debug(f"args.name is '{args.name}'")
    _logger.debug(f"args.courselet_dir is '{args.courselet_dir}'")

    courselet_dir = args.courselet_dir
    if courselet_dir[-1] == '/':
        courselet_dir = courselet_dir[:-1]

    name = args.name or os.path.basename(courselet_dir)
    output_file = args.output_file or f'{name}.zip'

    _logger.info(f"Curselet directory is '{courselet_dir}'")
    _logger.info(f"Name is '{name}'")
    _logger.info(f"Output-File is '{output_file}'")

    generator = CourseletGenerator()
    generator.import_directory(args.courselet_dir)

    generator.write_to(name, output_file)

    return


def run():
    """Entry point for console_scripts
    """
    return main(sys.argv[1:])


if __name__ == "__main__":
    exit(run())
