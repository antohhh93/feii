#!/usr/bin/python3

import click
from feii.main import class_structure, class_log, logging_level, generating_variables, generating_variables_for_fix_error, deleting_unnecessary_variables
from feii.cluster import Cluster

class_cluster = Cluster()
class_cluster.logger = class_log.logger

def start_retry_failed():
    class_cluster.retry_failed()

@click.command(short_help='Runs retry_failed for index.')
@click.option(
  '-l', '--log-level',
  default='info',
  show_default=True,
  expose_value=True,
  help='The output level of logs. \n\nOptions: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL'
)
def cli(log_level):
  """Runs retry_failed for index"""

  logging_level(log_level)
  class_log.logger.info("Started retry_failed for index")

  generating_variables()
  generating_variables_for_fix_error()
  deleting_unnecessary_variables()

  start_retry_failed()

if __name__ == "__main__":
  cli()
