#!/usr/bin/python3

import re
from feii.log import Log
from feii.config import Config
from feii.init import Init
from feii.structure import Structure

class Aliases(Structure):
  def add_alias_for_indices(self):
    for index in self.indices_no_alias:
      self.index = index['index']
      self.alias = index['index.alias']
      self.add_alias_for_index_and_check()

  def add_necessary_alias_for_indices(self):
    for index in self.indices_no_necessary_alias:
      self.index = index['index']
      self.alias = index['index.alias']
      self.add_alias_for_index_and_check()

  def add_alias_for_shrink_indices(self):
    for index in self.shrink_indices_no_alias:
      self.index = index['index']
      self.alias = re.sub(r'(shrink-)', '', index['index'])
      self.add_alias_for_index_and_check()

  def add_alias_for_indices_check_mode(self):
    for index in self.indices_no_alias:
      self.logger.warning("[check_mode] Adding an alias [{0}] for index [{1}]".format( index['index.alias'], index['index'] ))

  def add_necessary_alias_for_indices_check_mode(self):
    for index in self.indices_no_necessary_alias:
      self.logger.warning("[check_mode] Adding an alias [{0}] for index [{1}]".format( index['index.alias'], index['index'] ))

  def add_alias_for_shrink_indices_check_mode(self):
    for index in self.shrink_indices_no_alias:
      self.logger.warning("[check_mode] Adding an alias [{0}] for index [{1}]".format( re.sub(r'(shrink-)', '', index['index']), index['index'] ))

if __name__ == "__main__":
  class_config = Config
  class_config.index_pools = Init(count = 4).list_pools()
  class_config.ilm_list = class_config.index_pools[3].json()
  class_config.settings_list = class_config.index_pools[2].json()
  class_config.alias_list = class_config.index_pools[1].json()

  class_log = Log()
  class_log.remove_old_log_file()
  class_log.get_file_handler()
  class_log.get_stream_handler()
  class_log.get_logger()

  class_aliases = Aliases()
  class_aliases.logger = class_log.logger

  class_aliases.add_alias_for_indices()
  class_aliases.add_necessary_alias_for_indices()
  class_aliases.add_alias_for_shrink_indices()

  class_aliases.add_alias_for_indices_check_mode()
  class_aliases.add_necessary_alias_for_indices_check_mode()
  class_aliases.add_alias_for_shrink_indices_check_mode()
