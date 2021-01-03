#!/usr/bin/python3

import requests
from feii.log import Log
from feii.config import Config
from feii.init import Init
from feii.structure import Structure

class Delete(Structure):
  def debug_detail_index(self):
    self.index = 'test-000001'
    self.index_docs_count = 0

  def delete_empty_index(self):
    self.request = requests.delete("{0}/{1}".format( self.ELASTIC_URL, self.index ))

  def check_delete_empty_index(self):
    if self.status_request():
      self.logger.info("Deleting index [{0}] since it is empty - True".format( self.index ))
      return True

  def delete_indexes(self):
    for index in self.not_last_indices:
      self.index = index['index']
      if index['docs.count'] is None:
        continue

      if int(index['docs.count']) > 0:
        continue

      self.delete_empty_index()
      if not self.check_delete_empty_index():
        self.logger.error("Failed delete index [{0}]".format( self.index ))

  def delete_indexes_check_mode(self):
    for index in self.not_last_indices:
      if index['docs.count'] is None:
        continue

      if int(index['docs.count']) > 0:
        continue

      self.logger.warning("[check_mode] Deletion an empty index [{0}], documents count - {1}".format( index['index'], index['docs.count'] ))

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

  class_delete.delete_indexes()
  class_delete.delete_indexes_check_mode()
