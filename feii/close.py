#!/usr/bin/python3

from feii.config import Config
from feii.structure import Structure

class Close(Structure):
  def debug_detail_index(self):
    self.index = 'test-000001'
    self.index_docs_count = 0

  def close_expired_policy_indices(self):
    self.check_service_index()

    self.creating_array_age_ilm_policy()

    self.creating_array_index_with_age()
    self.update_array_index_with_age()

    self.creating_array_index_to_expired_policy()

    self.close_indexes_large_age()

  def close_expired_policy_indices_check_mode(self):
    self.creating_array_age_ilm_policy()

    self.creating_array_index_with_age()
    self.update_array_index_with_age()

    self.creating_array_index_to_expired_policy()

    for index in self.list_indexes_to_delete:
      self.logger.warning("[check_mode] Closing expired ilm policy index [{0}].".format( index ))

  def close_indexes_large_age(self):
    for index in self.list_indexes_to_delete:
      self.index = index
      if self.not_close_index_and_check() != False:
        Config.ilm_list['indices'].pop(index)
