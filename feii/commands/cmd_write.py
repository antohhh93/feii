#!/usr/bin/python3

import click
from feii.cli import WriteCLI

@click.command(
  cls=WriteCLI,
  short_help='Fix of writing in indices.',
  epilog="Run 'feii write COMMAND --help' for more information on a command."
)
def cli():
  """Fix of writing in indices"""
