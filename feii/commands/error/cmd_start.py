#!/usr/bin/python3

import click
from feii.main import class_structure, class_log, logging_level, updating_variables, generating_variables, generating_variables_for_fix_error, deleting_unnecessary_variables
from feii.error import FixError

class_fix_error = FixError()
class_fix_error.logger = class_log.logger

def start_fix_error_ilm_all(check_mode):
  if not check_mode:
    class_fix_error.fix_error_ilm_last_index()
    class_fix_error.fix_error_ilm_not_hot_phase_index()
    class_fix_error.fix_error_ilm_not_last_index()
    class_fix_error.fix_error_ilm_shrink_index()

def start_check_mode_fix_error_ilm_all(check_mode):
  if check_mode:
    class_fix_error.fix_error_ilm_last_index_in_check_mode()
    class_fix_error.fix_error_ilm_not_hot_phase_index_in_check_mode()
    class_fix_error.fix_error_ilm_not_last_index_in_check_mode()
    class_fix_error.fix_error_ilm_shrink_index_in_check_mode()

@click.command(short_help='Runs all commands in order.')
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
@click.option(
  '-p', '--path_to_file',
  default='',
  expose_value=True,
  help='path'
)
def cli(check_mode, log_level, path_to_file):
  """Runs all commands in order"""

  logging_level(log_level)
  class_log.logger.info("Started all fix ilm error")

  updating_variables(path_to_file)

  generating_variables()
  generating_variables_for_fix_error()
  deleting_unnecessary_variables()

  start_fix_error_ilm_all(check_mode)
  start_check_mode_fix_error_ilm_all(check_mode)

if __name__ == "__main__":
  cli()
