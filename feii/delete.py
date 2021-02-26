#!/usr/bin/python3

import re
import requests
from feii.log import Log
from feii.config import Config
from feii.init import Init
from feii.structure import Structure
from feii.function import Function

class Delete(Structure):
  def __init__(self,
    data_are_in_index: bool = False,
  ):
    super().__init__()
    self.data_are_in_index = data_are_in_index

  def debug_detail_index(self):
    self.index = 'test-000001'
    self.index_docs_count = 0

  def delete_empty_index(self):
    self.request = requests.delete("{0}/{1}".format( self.ELASTIC_URL, self.index ))

  def check_delete_empty_index(self):
    if self.status_request():
      self.logger.info("Deleting index [{0}] since it is empty - True".format( self.index ))
      return True

  def delete_not_last_indexes(self):
    for index in self.not_last_indices:
      self.index = index['index']
      if index['docs.count'] is None:
        continue

      if int(index['docs.count']) > 0:
        continue

      self.delete_empty_index()
      if not self.check_delete_empty_index():
        self.logger.error("Failed delete index [{0}]".format( self.index ))

  def delete_not_last_indexes_check_mode(self):
    for index in self.not_last_indices:
      if index['docs.count'] is None:
        continue

      if int(index['docs.count']) > 0:
        continue

      self.logger.warning("[check_mode] Deletion an empty not last index [{0}], documents count - {1}".format( index['index'], index['docs.count'] ))

  def delete_last_indexes(self):
    for delete_index in self.delete_last_indices:
      self.index = delete_index['index']
      self.data_are_in_index = False

      if delete_index['docs.count'] is None:
        continue

      if int(delete_index['docs.count']) > 0:
        continue

      self.check_prev_indices()

      if not self.data_are_in_index:
        self.index = delete_index['index']
        self.delete_empty_index()
        if not self.check_delete_empty_index():
          self.logger.error("Failed delete index [{0}]".format( self.index ))

  def delete_last_indexes_check_mode(self):
    for delete_index in self.delete_last_indices:
      self.index = delete_index['index']
      self.data_are_in_index = False

      if delete_index['docs.count'] is None:
        continue

      if int(delete_index['docs.count']) > 0:
        continue

      self.check_prev_indices()

      if not self.data_are_in_index:
        self.logger.warning("[check_mode] Deletion an empty last index [{0}], documents count - {1}".format( delete_index['index'], delete_index['docs.count'] ))

  def check_prev_indices(self):
    for x in range(3):
      self.prev_index_to_check = {}

      self.find_prev_index()
      self.without_shrink_prev_index = re.sub(r'(shrink-)', '', self.prev_index)

      if self.without_shrink_prev_index in Config.alias_list:
        self.creating_array_not_shrink_prev_index()

      if 'shrink-' + self.without_shrink_prev_index in Config.alias_list:
        self.creating_array_shrink_prev_index()

      self.check_empty_docs_in_prev_index()
      self.check_count_docs_in_prev_index()

      if not self.without_shrink_prev_index in Config.alias_list:
        self.index = self.without_shrink_prev_index
        continue

      if not 'shrink-' + self.without_shrink_prev_index in Config.alias_list:
        self.index = self.without_shrink_prev_index
        continue

  def check_empty_docs_in_prev_index(self):
    if 'docs.count' in self.prev_index_to_check and self.prev_index_to_check['docs.count'] is None:
      self.data_are_in_index = True

  def check_count_docs_in_prev_index(self):
    if 'docs.count' in self.prev_index_to_check and int(self.prev_index_to_check['docs.count']) > 0:
      self.data_are_in_index = True

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

  class_delete = Delete()
  class_delete.debug_detail_index()

  class_delete.logger = class_log.logger

  class_delete.delete_not_last_indexes()
  class_delete.delete_not_last_indexes_check_mode()

  class_delete.delete_last_indexes()
  class_delete.delete_last_indexes_check_mode()
