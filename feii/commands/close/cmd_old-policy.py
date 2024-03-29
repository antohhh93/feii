#!/usr/bin/python3

import click
from feii.main import class_structure, class_log, logging_level, updating_variables, generating_variables_for_indices, generating_variables_for_close, deleting_unnecessary_variables
from feii.close import Close

class_close = Close()
class_close.logger = class_log.logger

def start_close_expired_policy_indices(check_mode):
  if not check_mode:
    class_close.close_expired_policy_indices()

def start_check_mode_close_expired_policy_indices(check_mode):
  if check_mode:
    class_close.close_expired_policy_indices_check_mode()

@click.command(short_help='Close expired ilm policy indexes.')
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
def cli(check_mode, log_level, path_to_file):
  """Close expired ilm policy indexes"""

  logging_level(log_level)
  class_log.logger.info("Started close expired ilm policy indexes")

  updating_variables(path_to_file)

  generating_variables_for_indices()
  generating_variables_for_close()
  deleting_unnecessary_variables()

  start_close_expired_policy_indices(check_mode)
  start_check_mode_close_expired_policy_indices(check_mode)

if __name__ == "__main__":
  cli()
