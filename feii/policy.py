#!/usr/bin/python3

import re
import requests
from feii.structure import Structure

class Policy(Structure):
  def __init__(self,
    index_or_alias: str = ""
  ):
    super().__init__()
    self.index_or_alias = index_or_alias

  def update_ilm_policy(self, set_index: str = '', set_alias: str = '', set_policy: str = ''):
    self.check_service_index()

    self.index = set_index
    self.alias = set_alias
    self.policy = set_policy

    self.check_on_alias()
    self.check_on_index()

    if self.index and not self.check_for_latest_index():
      self.logger.warning("The specified index [{0}] is not the last one".format( self.index ))
      self.find_latest_index()

    if self.alias:
      self.find_latest_index()

    self.remove_ilm_policy()
    self.check_remove_ilm_policy()

    self.adding_new_ilm_policy()
    self.check_adding_new_ilm_policy()

    self.creating_array_index_to_remove_by_ilm_policy()
    self.writing_to_service_index(self.indices_to_remove_by_ilm_policy, self.SERVICE_INDEX, indexes = self.indices_to_remove_by_ilm_policy, policy = self.policy)
    self.check_writing_to_service_index(self.indices_to_remove_by_ilm_policy, self.SERVICE_INDEX)

  def update_ilm_policy_check_mode(self, set_index: str = '', set_alias: str = '', set_policy: str = ''):
    self.index = set_index
    self.alias = set_alias
    self.policy = set_policy

    self.check_on_alias()
    self.check_on_index()

    if self.index and not self.check_for_latest_index():
      self.logger.warning("The specified index [{0}] is not the last one".format( self.index ))
      self.find_latest_index()

    if self.alias:
      self.find_latest_index()

    self.logger.warning("[check_mode] Updating the index [{0}] policy on the [{1}]".format( self.index, self.policy ))

  def check_for_latest_index(self):
    for index in self.last_indices:
      if self.index == index['index']:
        return True

  def check_on_alias(self):
    if not self.index and self.alias:
      self.index_or_alias = re.sub(r'(shrink-)', '', self.alias)

  def check_on_index(self):
    if not self.alias and self.index:
      self.index_or_alias = re.sub(r'(shrink-)', '', self.index[:-7])

  def find_latest_index(self):
    for index in self.last_indices:
      if self.index_or_alias == index['index.alias']:
        self.index = index['index']

  def add_exception_ilm_policy(self, set_alias: str = ''):
    self.check_service_index(service_index_name = self.SERVICE_INDEX_EXCEPTION)

    self.writing_to_service_index(set_alias, self.SERVICE_INDEX_EXCEPTION, aliases = set_alias)
    self.check_writing_to_service_index(set_alias, self.SERVICE_INDEX_EXCEPTION)

  def writing_to_service_index(self, check=False, service_index_name=None, **kwargs):
    if check and service_index_name:
      self.request = requests.post("{0}/{1}/_doc/?timeout={2}".format( self.ELASTIC_URL, service_index_name, self.MASTER_TIMEOUT ), json=kwargs ) if kwargs else False

  def check_writing_to_service_index(self, check=False, service_index_name=None):
    if check and service_index_name and self.request and self.status_request():
      self.logger.info("The data is written to the service index [{0}]".format( service_index_name ))
      return True
