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
