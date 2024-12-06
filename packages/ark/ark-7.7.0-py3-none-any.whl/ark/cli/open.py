# ------------------------------------------------------------------------------
# This module contains the logic for the 'open' command.
# ------------------------------------------------------------------------------

import ark
import sys
import webbrowser
import os

from .. import events

helptext = """
Usage: ark open [url]

  This command opens the output file corresponding to the specified @root/ url
  directly in the default web browser. If no url has been specified it defaults
  to opening the site root.

Arguments:
  [url]             The @root/ url to open. Defaults to the site root.

Flags:
  -h, --help        Print this command's help text and exit.
"""


@ark.events.register(events.Event.CLI)
def register_command(argparser):
    argparser.command("open", helptext, cmd_callback)


def cmd_callback(cmd_name, cmd_parser):
    if not ark.site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    if not os.path.isdir(ark.site.out()):
        sys.exit("Error: cannot locate the site's output directory.")

    arg = cmd_parser.args[0] if cmd_parser.args else "@root/"
    if (node := ark.nodes.node(arg)):
        url  = "file://" + node.get_output_filepath()
        webbrowser.open(url)
    else:
        sys.exit(f"Error: unknown url '{arg}'.")

    sys.exit()
