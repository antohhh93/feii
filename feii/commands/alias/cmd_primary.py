#!/usr/bin/python3

import click
from feii.main import class_structure, class_log, logging_level, updating_variables, generating_variables, generating_variables_for_alias, generating_variables_for_alias_not_srink, deleting_unnecessary_variables
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
  help='Set the logging level ("debug"|"info"|"warning"|"error"|"critical")'
)
@click.option(
  '-n', '--not-shrink',
  is_flag=True,
  expose_value=True,
  help='Indexes only, no shrink.'
)
@click.option(
  '-p', '--path_to_file',
  default='',
  expose_value=True,
  help='path'
)
def cli(check_mode, log_level, not_shrink, path_to_file):
  """Adding a primary alias for all indexes"""

  logging_level(log_level)
  class_log.logger.info("Started adding a primary alias for all indexes")

  updating_variables(path_to_file)

  generating_variables()
  if not_shrink:
    generating_variables_for_alias_not_srink()
  else:
    generating_variables_for_alias()
  deleting_unnecessary_variables()

  start_add_necessary_alias_for_indices(check_mode)
  start_check_mode_add_necessary_alias_for_indices(check_mode)

if __name__ == "__main__":
  cli()
