#!/usr/bin/python3

import re
import time
import requests
from feii.log import Log
from feii.config import Config
from feii.init import Init
from feii.index import Index
from feii.request import Request
from feii.ilm import Ilm
from feii.alias import Alias
from feii.cluster import Cluster
from feii.function import Function

class Structure(Index, Ilm, Alias, Function, Cluster, Request):
  def cluster_status(self):
    while True:
      self.get_status_cluster()

      if not self.check_count_relocating_shards_in_cluster():
        self.logger.warning("Number of relocating shards reaches {0}".format( self.cluster['relocating_shards'] ))
        self.retry += 1
        self.time_sleep()
        continue

      if not self.check_count_pending_tasks_in_cluster():
        self.logger.warning("Number of pending tasks reaches {0}".format( self.cluster['number_of_pending_tasks'] ))
        self.retry += 1
        self.time_sleep()
        continue

      if self.check_count_relocating_shards_in_cluster() and self.check_count_pending_tasks_in_cluster():
        self.retry = 0
        break

  def rollover_index_and_check(self):
    self.cluster_status()
    self.rollover_index()
    self.find_next_index()
    self.check_create_next_index()
    return self.check_rollover_index()

  def update_timeout_index_and_check(self):
    self.cluster_status()
    self.update_index()
    return self.check_update_index()

  def add_write_disable_for_index_and_check(self):
    self.add_alias_for_index_and_write_disable()
    self.cluster_status()
    self.request_add_alias_for_index()
    return self.check_disable_write_for_index()

  def add_write_enable_for_index_and_check(self):
    self.add_alias_for_index_and_write_enable()
    self.cluster_status()
    self.request_add_alias_for_index()
    return self.check_enable_write_for_index()

  def ilm_retry_index_and_check(self):
    self.cluster_status()
    self.ilm_retry_for_index()
    return self.check_ilm_retry_for_index()

  def next_step_for_index_and_check(self):
    self.current_ilm_info_for_index()
    self.create_current_ilm_info_for_index()
    self.next_step_for_not_shrink_index()
    self.next_step_for_shrink_index()
    self.cluster_status()
    self.request_next_step_for_index()
    return self.check_next_step_for_index()

  def next_step_for_not_shrink_index(self):
    if not self.index_pattern.match(self.index).group(1):
      self.next_step_index_in_warm()

  def next_step_for_shrink_index(self):
    if self.index_pattern.match(self.index).group(1):
      self.next_step_index_in_cold()

  def not_next_step_for_index_and_check(self):
    if not self.next_step_for_index_and_check():
      self.logger.error("Failed next step to index [{0}]".format( self.index ))

  def create_new_index_and_check(self):
    self.find_next_index()
    self.cluster_status()
    self.create_new_index()
    return self.check_create_new_index()

  def add_alias_for_index_and_check(self):
    self.add_alias_for_index()
    self.cluster_status()
    self.request_add_alias_for_index()
    return self.check_add_alias_for_index()

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

  class_structure = Structure()
  class_structure.logger = class_log.logger

  class_structure.creating_array_index_details_in_open()
  class_structure.creating_array_index_to_remove()
  class_structure.remove_invalid_index_name_in_array()
  class_structure.creating_array_indices()
  class_structure.creating_array_max_indices()

  del(class_structure.index_details)
  del(class_structure.index_to_remove)

  class_structure.creating_array_invalid_size_index()
  class_structure.remove_invalid_indexes_in_array( class_structure.invalid_size_indices )

  class_structure.creating_array_unmanaged_index()
  class_structure.remove_invalid_indexes_in_array( class_structure.unmanaged_indices )

  class_structure.creating_array_not_hot_box_index()
  class_structure.remove_invalid_indexes_in_array( class_structure.not_hot_box_indices )

  class_structure.creating_array_not_hot_phase_index()
  class_structure.remove_invalid_indexes_in_array( class_structure.not_hot_phase_indices )

  class_structure.creating_array_shrink_index()
  class_structure.remove_invalid_indexes_in_array( class_structure.shrink_indices )

  class_structure.creating_array_last_index()
  class_structure.creating_array_not_last_index()
  class_structure.creating_array_last_shrink_index()

  del(class_structure.invalid_size_indices)
  del(class_structure.unmanaged_indices)
  del(class_structure.not_hot_box_indices)
  del(class_structure.not_hot_phase_indices)

  class_structure.creating_array_no_alias_in_index()
  class_structure.creating_array_no_necessary_alias_in_index()
  class_structure.creating_array_no_shrink_alias_in_index()
