#!/usr/bin/python3

import re
import requests
from feii.log import Log
from feii.config import Config
from feii.init import Init
from feii.request import Request
from feii.function import Function

class Alias(Config, Request):
  def __init__(self,
  ):
    super().__init__()

  def debug_detail_index(self):
    self.alias = 'test'
    self.index = 'test-000001'

  def add_alias_for_index(self):
    self.data = { "actions": [ { "add": { "index": self.index, "alias": self.alias } } ] }

  def add_alias_for_index_and_write_disable(self):
    self.data = { "actions": [ { "add": { "index": self.index, "alias": self.alias, "is_write_index": False } } ] }

  def add_alias_for_index_and_write_enable(self):
    self.data = { "actions": [ { "add": { "index": self.index, "alias": self.alias, "is_write_index": True } } ] }

  def request_add_alias_for_index(self):
    self.request = requests.post("{0}/_aliases?master_timeout={1}".format( self.ELASTIC_URL, self.MASTER_TIMEOUT ), json=self.data )

  def check_add_alias_for_index(self):
    if self.status_request():
      self.logger.info("Alias [{0}] was added to index [{1}]".format( self.alias, self.index ))
      return True

  def check_disable_write_for_index(self):
    if self.status_request():
      self.logger.info("Writing is disabled for the index [{0}]".format( self.index ))
      return True

  def check_enable_write_for_index(self):
    if self.status_request():
      self.logger.info("Writing is enabled for the index [{0}]".format( self.index ))
      return True

if __name__ == "__main__":
  class_config = Config
  class_config.index_pools = Init(count = 4).list_pools()
  class_config.alias_list = class_config.index_pools[1].json()

  class_log = Log()
  class_log.remove_old_log_file()
  class_log.get_file_handler()
  class_log.get_stream_handler()
  class_log.get_logger()

  class_function = Function()
  class_function.debug_detail_index()

  class_alias = Alias()
  class_alias.debug_detail_index()
  class_alias.index = class_function.find_next_index()

  class_alias.logger = class_log.logger

  class_alias.add_alias_for_index()
  class_alias.request_add_alias_for_index()
  class_alias.check_add_alias_for_index()

  class_alias.debug_detail_index()
  class_alias.add_alias_for_index_and_write_disable()
  class_alias.request_add_alias_for_index()
  class_alias.check_disable_write_for_index()

  class_alias.index = class_function.find_next_index()
  class_alias.add_alias_for_index_and_write_enable()
  class_alias.request_add_alias_for_index()
  class_alias.check_enable_write_for_index()
