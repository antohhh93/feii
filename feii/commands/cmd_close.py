#!/usr/bin/python3

import click
from feii.cli import CloseCLI

@click.command(
  cls=CloseCLI,
  short_help='Closing Indexes.',
  epilog="Run 'feii delete COMMAND --help' for more information on a command."
)
def cli():
  """Closing Indexes"""
