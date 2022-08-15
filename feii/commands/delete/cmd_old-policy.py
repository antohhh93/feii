#!/usr/bin/python3

import click
from feii.main import class_structure, class_log, logging_level, updating_variables, generating_variables_for_indices, generating_variables_for_delete, deleting_unnecessary_variables
from feii.delete import Delete
from feii.close import Close

class_delete = Delete()
class_delete.logger = class_log.logger

class_close = Close()
class_close.logger = class_log.logger

def start_delete_expired_policy_indices(check_mode, close):
  if not check_mode and not close:
    class_delete.delete_expired_policy_indices()
  if not check_mode and close:
    class_close.close_expired_policy_indices()

def start_check_mode_delete_expired_policy_indices(check_mode, close):
  if check_mode and not close:
    class_delete.delete_expired_policy_indices_check_mode()
  if check_mode and close:
    class_close.close_expired_policy_indices_check_mode()

@click.command(short_help='Deleting expired ilm policy indexes.')
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
  '-P', '--path-to-file',
  default='',
  expose_value=True,
  help='path'
)
@click.option(
  '--close',
  is_flag=True,
  expose_value=True,
  help='Allows you to close the index without deleting'
)
def cli(check_mode, close, log_level, path_to_file):
  """Deleting expired ilm policy indexes"""

  logging_level(log_level)
  class_log.logger.info("Started deleting expired ilm policy indexes")

  updating_variables(path_to_file)

  generating_variables_for_indices()
  generating_variables_for_delete()
  deleting_unnecessary_variables()

  start_delete_expired_policy_indices(check_mode, close)
  start_check_mode_delete_expired_policy_indices(check_mode, close)

if __name__ == "__main__":
  cli()
