#!/usr/bin/python3
from __future__ import absolute_import

import argparse
import os
import sys

import wx


# python 2 and 3 compatibility hack
def to_utf(s):
    if isinstance(s, bytes):
        return s.decode('utf-8')
    else:
        return s


if __name__ == "__main__":
    # Add ../ to the path
    # Works if this script is executed without installing the module
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(script_dir))

    os.environ['INTERACTIVE_HTML_BOM_CLI_MODE'] = 'True'
    import InteractiveHtmlBom

    from InteractiveHtmlBom.core import ibom
    from InteractiveHtmlBom.core.config import Config
    from InteractiveHtmlBom.ecad import get_parser_by_extension
    from InteractiveHtmlBom.version import version

    app = wx.App()

    parser = argparse.ArgumentParser(
            description='KiCad InteractiveHtmlBom plugin CLI.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file',
                        type=lambda s: to_utf(s),
                        help="KiCad PCB file")
    config = Config(version)
    config.add_options(parser, config.FILE_NAME_FORMAT_HINT)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        print("File %s does not exist." % args.file)
        exit(1)
    print("Loading %s" % args.file)
    logger = ibom.Logger(cli=True)
    parser = get_parser_by_extension(os.path.abspath(args.file), config, logger)
    if args.show_dialog:
        ibom.run_with_dialog(parser, config, logger)
    else:
        config.set_from_args(args)
        ibom.main(parser, config, logger)
