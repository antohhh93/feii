#!/usr/bin/python3

from feii.config import Config
from feii.structure import Structure

class Close(Structure):
  def debug_detail_index(self):
    self.index = 'test-000001'
    self.index_docs_count = 0

  def close_expired_policy_indices(self):
    self.check_service_index(service_index_name = self.SERVICE_INDEX_EXCEPTION)

    self.creating_array_age_ilm_policy()

    self.creating_array_indexes_with_policy_age()
    self.creating_array_indexes_with_policy_age_to_close()
    self.creating_array_indexes_expired_policy_to_close()

    self.close_indexes_large_age()

  def close_expired_policy_indices_check_mode(self):
    self.creating_array_age_ilm_policy()

    self.creating_array_indexes_with_policy_age()
    self.creating_array_indexes_with_policy_age_to_close()
    self.creating_array_indexes_expired_policy_to_close()

    for index in self.list_indices_to_close:
      self.logger.warning("[check_mode] Closing expired ilm policy index [{0}] age exceeds - [{1}].".format( index['index'], index['policy.age'] ))

  def close_indexes_large_age(self):
    for index in self.list_indices_to_close:
      self.index = index['index']
      if self.not_close_index_and_check() != False:
        Config.ilm_list['indices'].pop(index['index'])
