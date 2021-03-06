#!/usr/bin/python3

import re
import requests
from feii.log import Log
from feii.config import Config
from feii.init import Init
from feii.request import Request
from feii.function import Function

class Index(Config, Request):
  def __init__(self,
    indices: str = [],
    index_details: str = [],
    shrink_indices: str = [],
    index_to_remove: str = [],
    index_current_num: str = {},
    invalid_size_indices: str = [],
    unmanaged_indices: str = [],
    not_hot_box_indices: str = [],
    not_hot_phase_indices: str = [],
    last_indices: str = [],
    not_last_indices: str = [],
    last_shrink_indices: str = [],
    not_last_shrink_indices: str = [],
    indices_no_alias: str = [],
    indices_no_necessary_alias: str = [],
    shrink_indices_no_alias: str = [],
    indices_not_write: str = [],
    error_ilm_indices: str = [],
    error_ilm_shrink_indices: str = [],
    error_ilm_last_indices: str = [],
    error_ilm_not_last_indices: str = [],
    error_ilm_not_hot_phase_indices: str = [],
    delete_last_indices: str = [],
    timeout_last_indices: str = [],
    timeout_not_last_indices: str = [],
    prev_index_to_check: str = {},
    without_shrink_prev_index: str = '',
    new_index_name: str = '',
  ):
    super().__init__()
    self.indices = indices
    self.index_details = index_details
    self.shrink_indices = shrink_indices
    self.index_to_remove = index_to_remove
    self.index_current_num = index_current_num
    self.invalid_size_indices = invalid_size_indices
    self.unmanaged_indices = unmanaged_indices
    self.not_hot_box_indices = not_hot_box_indices
    self.not_hot_phase_indices = not_hot_phase_indices
    self.last_indices = last_indices
    self.not_last_indices = not_last_indices
    self.last_shrink_indices = last_shrink_indices
    self.not_last_shrink_indices = not_last_shrink_indices
    self.indices_no_alias = indices_no_alias
    self.indices_no_necessary_alias = indices_no_necessary_alias
    self.shrink_indices_no_alias = shrink_indices_no_alias
    self.indices_not_write = indices_not_write
    self.error_ilm_indices = error_ilm_indices
    self.error_ilm_shrink_indices = error_ilm_shrink_indices
    self.error_ilm_last_indices = error_ilm_last_indices
    self.error_ilm_not_last_indices = error_ilm_not_last_indices
    self.error_ilm_not_hot_phase_indices = error_ilm_not_hot_phase_indices
    self.delete_last_indices = delete_last_indices
    self.timeout_last_indices = timeout_last_indices
    self.timeout_not_last_indices = timeout_not_last_indices
    self.prev_index_to_check = prev_index_to_check
    self.without_shrink_prev_index = without_shrink_prev_index
    self.new_index_name = new_index_name

  def debug_detail_index(self):
    self.alias = 'test'
    self.index = 'test-000001'

  def creating_array_index_details_in_open(self):
    for details in Config.index_pools[0].json():
      if details['status'] == 'open':
        self.index_details.append(details)

  def creating_array_index_to_remove(self):
    for details in self.index_details:
      if not self.index_pattern.match(details['index']):
        self.index_to_remove.append(details)
        self.logger.warning("[{0}] encountered a strange index name".format(details['index']))

  def remove_invalid_index_name_in_array(self):
    for details in self.index_to_remove:
      self.index_details.remove(details)

  def creating_array_indices(self):
    for details in self.index_details:
      index_details = details.copy()
      index_details['number'] = int(self.index_pattern.match(details['index']).group(3))
      index_details['index.alias'] = self.index_pattern.match(details['index']).group(2)
      self.indices.append(index_details)

  def creating_array_max_indices(self):
    for details in self.index_details:
      if self.index_current_num.get(self.index_pattern.match(details['index']).group(2), -1) < int(self.index_pattern.match(details['index']).group(3)):
        self.index_current_num[self.index_pattern.match(details['index']).group(2)] = int(self.index_pattern.match(details['index']).group(3))

  def creating_array_invalid_size_index(self):
    for index in self.indices:
      if index['pri.store.size'] is None or int(index['pri.store.size']) <= self.MAX_CURRENT_INDEX_SIZE_GB:
        self.invalid_size_indices.append(index)

  def creating_array_unmanaged_index(self):
    for index in self.indices:
      if not Config.ilm_list['indices'][index['index']]['managed']:
        self.unmanaged_indices.append(index)
        self.logger.warning("[{0}] not management".format(index['index']))

  def creating_array_not_hot_box_index(self):
    for index in self.indices:
      if Config.settings_list[index['index']]['settings']['index']['routing']['allocation']['require']['box_type'] != 'hot':
        self.not_hot_box_indices.append(index)

  def creating_array_not_hot_phase_index(self):
    for index in self.indices:
      if Config.ilm_list['indices'][index['index']]['phase'] != 'hot':
        self.not_hot_phase_indices.append(index)

  def creating_array_shrink_index(self):
    for index in self.indices:
      if self.index_pattern.match(index['index']).group(1):
        self.shrink_indices.append(index)

  def creating_array_last_index(self):
    for index in self.indices:
      if self.index_current_num[index['index.alias']] == index['number']:
        self.last_indices.append(index)

  def creating_array_not_last_index(self):
    for index in self.indices:
      if self.index_current_num[index['index.alias']] != index['number']:
        self.not_last_indices.append(index)

  def creating_array_last_shrink_index(self):
    for index in self.shrink_indices:
      if self.index_current_num[index['index.alias']] == index['number']:
        self.last_shrink_indices.append(index)

  def creating_array_not_last_shrink_index(self):
    for index in self.shrink_indices:
      if self.index_current_num[index['index.alias']] != index['number']:
        self.not_last_shrink_indices.append(index)

  def creating_array_no_alias_in_index(self):
    for index in self.indices:
      if not Config.alias_list[index['index']]['aliases']:
        self.indices_no_alias.append(index)

  def creating_array_no_necessary_alias_in_index(self):
    for index in self.indices:
      if not index['index.alias'] in Config.alias_list[index['index']]['aliases']:
        self.indices_no_necessary_alias.append(index)

  def creating_array_no_shrink_alias_in_index(self):
    for index in self.shrink_indices:
      alias = re.sub(r'(shrink-)', '', index['index'])
      if not alias in Config.alias_list[index['index']]['aliases']:
        self.shrink_indices_no_alias.append(index)

  def creating_array_not_write_in_index(self):
    for index in self.indices:
      if not 'is_write_index' in Config.alias_list[index['index']]['aliases'][index['index.alias']]:
        self.indices_not_write.append(index)

  def creating_array_error_ilm_index(self):
    for index in self.indices:
      if 'step' in Config.ilm_list['indices'][index['index']] and Config.ilm_list['indices'][index['index']]['step'] == "ERROR":
        index_details = index.copy()
        index_details['error.type'] = Config.ilm_list['indices'][index['index']]['step_info']['type']
        index_details['error.reason'] = Config.ilm_list['indices'][index['index']]['step_info']['reason']
        self.error_ilm_indices.append(index_details)

  def creating_array_error_ilm_shrink_index(self):
    for index in self.error_ilm_indices:
      if self.index_pattern.match(index['index']).group(1):
        self.error_ilm_shrink_indices.append(index)

  def creating_array_error_ilm_last_indices(self):
    for index in self.error_ilm_indices:
      if self.index_current_num[index['index.alias']] == index['number']:
        self.error_ilm_last_indices.append(index)

  def creating_array_error_ilm_not_last_indices(self):
    for index in self.error_ilm_indices:
      if self.index_current_num[index['index.alias']] != index['number']:
        self.error_ilm_not_last_indices.append(index)

  def creating_array_error_ilm_not_hot_phase_indices(self):
    for index in self.error_ilm_indices:
      if Config.ilm_list['indices'][index['index']]['phase'] != 'hot':
        self.error_ilm_not_hot_phase_indices.append(index)

  def creating_array_delete_index(self):
    for index in self.last_indices:
      if int(self.index_pattern.match(index['index']).group(3)) > 3:
        self.delete_last_indices.append(index)

  def creating_array_not_shrink_prev_index(self):
    for index_array in self.indices:
      if index_array['index'] == self.without_shrink_prev_index:
        self.prev_index_to_check['index'] = self.without_shrink_prev_index
        self.prev_index_to_check['docs.count'] = index_array['docs.count']

  def creating_array_shrink_prev_index(self):
    for index_array in self.indices:
      if index_array['index'] == 'shrink-' + self.without_shrink_prev_index:
        self.prev_index_to_check['index'] = 'shrink-' + self.without_shrink_prev_index
        self.prev_index_to_check['docs.count'] = index_array['docs.count']

  def creating_array_timeout_last_index(self):
    for index in self.last_indices:
      if not 'unassigned' in Config.settings_list[index['index']]['settings']['index'] or Config.settings_list[index['index']]['settings']['index']['unassigned']['node_left']['delayed_timeout'] != self.HOT_DELAYED_TIMEOUT:
        self.timeout_last_indices.append(index)

  def creating_array_timeout_not_last_index(self):
    for index in self.not_last_indices:
      if not 'unassigned' in Config.settings_list[index['index']]['settings']['index'] or Config.settings_list[index['index']]['settings']['index']['unassigned']['node_left']['delayed_timeout'] != self.COLD_DELAYED_TIMEOUT:
        self.timeout_not_last_indices.append(index)

  def remove_invalid_indexes_in_array(self, indexes_array: str = []):
    for index in indexes_array:
      self.indices.remove(index)

  def remove_invalid_error_ilm_indexes_in_array(self, indexes_array: str = []):
    for index in indexes_array:
      self.error_ilm_indices.remove(index)

  def create_new_index(self):
    self.new_index_name = re.sub(r'(shrink-)', '', self.next_index)
    data = { "aliases": { self.alias: { "is_write_index" : False } } }
    self.request = requests.put("{0}/{1}?master_timeout={2}".format( self.ELASTIC_URL, self.new_index_name, self.MASTER_TIMEOUT), json=data)

  def check_create_new_index(self):
    if self.status_request():
      self.logger.info("Create new index [{0}] - True".format( self.new_index_name ))
      return True
