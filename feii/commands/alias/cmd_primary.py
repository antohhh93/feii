#!/usr/bin/python3

import click
from feii.main import class_structure, class_log, logging_level, generating_variables, generating_variables_for_alias, deleting_unnecessary_variables
from feii.aliases import Aliases

class_aliases = Aliases()
class_aliases.logger = class_log.logger

def start_add_necessary_alias_for_indices(check_mode):
  if not check_mode:
    class_aliases.add_necessary_alias_for_indices()

def start_check_mode_add_necessary_alias_for_indices(check_mode):
  if check_mode:
    class_aliases.add_necessary_alias_for_indices_check_mode()

@click.command(short_help='Adding an primary alias for all indexes.')
@click.option(
  '-c', '--check-mode',
  is_flag=True,
  expose_value=True,
  help='Only displaying actions, without performing them.'
)
@click.option(
  '-l', '--log-level',
  default='info',
  show_default=True,
  expose_value=True,
  help='The output level of logs. \n\nOptions: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL'
)
def cli(check_mode, log_level):
  """Adding an primary alias for all indexes"""

  logging_level(log_level)
  class_log.logger.info("Started adding an primary alias for all indexes")

  generating_variables()
  generating_variables_for_alias()
  deleting_unnecessary_variables()

  start_add_necessary_alias_for_indices(check_mode)
  start_check_mode_add_necessary_alias_for_indices(check_mode)

if __name__ == "__main__":
  cli()