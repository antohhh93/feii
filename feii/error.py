#!/usr/bin/python3

from feii.log import Log
from feii.config import Config
from feii.init import Init
from feii.structure import Structure

class FixError(Structure):
  def not_ilm_retry_index_and_check(self):
    if not self.ilm_retry_index_and_check():
      self.logger.error("Failed ilm retry to next index [{0}]".format( self.index ))

  def remove_block_index_and_check(self):
    self.remove_block_index()
    return self.check_remove_block_index()

  def not_remove_block_index_and_check(self):
    if not self.remove_block_index_and_check():
      self.logger.error("Failed remove cluster block to index [{0}]".format( self.index ))
      return True

  def fix_error_ilm_last_index(self):
    for index in self.error_ilm_last_indices:
      self.index = index['index']

      if index['error.type'] == "process_cluster_event_timeout_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "illegal_state_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "index_closed_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "illegal_argument_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "resource_already_exists_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "cluster_block_exception":
        if self.not_remove_block_index_and_check():
          continue
        self.not_ilm_retry_index_and_check()

  def fix_error_ilm_not_hot_phase_index(self):
    for index in self.error_ilm_not_hot_phase_indices:
      self.index = index['index']

      if index['error.type'] == "process_cluster_event_timeout_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "illegal_state_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "index_closed_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "illegal_argument_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "resource_already_exists_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "cluster_block_exception":
        if self.not_remove_block_index_and_check():
          continue
        self.not_ilm_retry_index_and_check()

  def fix_error_ilm_not_last_index(self):
    for index in self.error_ilm_not_last_indices:
      self.index = index['index']

      if index['error.type'] == "process_cluster_event_timeout_exception":
        self.not_next_step_for_index_and_check()

      if index['error.type'] == "illegal_state_exception":
        self.not_next_step_for_index_and_check()

      if index['error.type'] == "index_closed_exception":
        self.not_next_step_for_index_and_check()

      if index['error.type'] == "illegal_argument_exception":
        self.not_next_step_for_index_and_check()

      if index['error.type'] == "resource_already_exists_exception":
        self.not_next_step_for_index_and_check()

      if index['error.type'] == "cluster_block_exception":
        if self.not_remove_block_index_and_check():
          continue
        self.not_next_step_for_index_and_check()

  def fix_error_ilm_shrink_index(self):
    for index in self.error_ilm_shrink_indices:
      self.index = index['index']

      if index['error.type'] == "process_cluster_event_timeout_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "index_closed_exception":
        self.not_ilm_retry_index_and_check()

      if index['error.type'] == "null_pointer_exception":
        self.not_ilm_retry_index_and_check()

  def fix_error_ilm_last_index_in_check_mode(self):
    for index in self.error_ilm_last_indices:
      self.logger.warning("[check_mode] Fix ilm error [{0}] for index [{1}]".format( index['error.type'], index['index'] ))

  def fix_error_ilm_not_hot_phase_index_in_check_mode(self):
    for index in self.error_ilm_not_hot_phase_indices:
      self.logger.warning("[check_mode] Fix ilm error [{0}] for index [{1}]".format( index['error.type'], index['index'] ))

  def fix_error_ilm_not_last_index_in_check_mode(self):
    for index in self.error_ilm_not_last_indices:
      self.logger.warning("[check_mode] Fix ilm error [{0}] for index [{1}]".format( index['error.type'], index['index'] ))

  def fix_error_ilm_shrink_index_in_check_mode(self):
    for index in self.error_ilm_shrink_indices:
      self.logger.warning("[check_mode] Fix ilm error [{0}] for index [{1}]".format( index['error.type'], index['index'] ))

if __name__ == "__main__":
  class_config = Config
  class_config.index_pools = Init(count = 4).list_pools()
  class_config.ilm_list = class_config.index_pools[3].json()
  class_config.settings_list = class_config.index_pools[2].json()

  class_log = Log()
  class_log.remove_old_log_file()
  class_log.get_file_handler()
  class_log.get_stream_handler()
  class_log.get_logger()

  class_fix_error = FixError()
  class_fix_error.logger = class_log.logger

  class_fix_error.creating_array_index_details_in_open()
  class_fix_error.creating_array_index_to_remove()
  class_fix_error.remove_invalid_index_name_in_array()
  class_fix_error.creating_array_indices()
  class_fix_error.creating_array_max_indices()

  del(class_fix_error.index_details)
  del(class_fix_error.index_to_remove)

  class_fix_error.creating_array_unmanaged_index()
  class_fix_error.remove_invalid_indexes_in_array( class_fix_error.unmanaged_indices )

  class_fix_error.creating_array_error_ilm_index()
  class_fix_error.creating_array_error_ilm_shrink_index()
  class_fix_error.remove_invalid_error_ilm_indexes_in_array( class_fix_error.error_ilm_shrink_indices )
  class_fix_error.creating_array_error_ilm_last_indices()

  class_fix_error.remove_invalid_error_ilm_indexes_in_array( class_fix_error.error_ilm_last_indices )
  class_fix_error.creating_array_error_ilm_not_hot_phase_indices()

  class_fix_error.remove_invalid_error_ilm_indexes_in_array( class_fix_error.error_ilm_not_hot_phase_indices )
  class_fix_error.creating_array_error_ilm_not_last_indices()

  class_fix_error.fix_error_ilm_last_index()
  class_fix_error.fix_error_ilm_not_hot_phase_index()
  class_fix_error.fix_error_ilm_not_last_index()
  class_fix_error.fix_error_ilm_shrink_index()

  class_fix_error.fix_error_ilm_last_index_in_check_mode()
  class_fix_error.fix_error_ilm_not_hot_phase_index_in_check_mode()
  class_fix_error.fix_error_ilm_not_last_index_in_check_mode()
  class_fix_error.fix_error_ilm_shrink_index_in_check_mode()
