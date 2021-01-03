#!/usr/bin/python3

import re

class Config:
  def __init__(self,
    ELASTIC_URL: str = 'http://localhost:9200',
    ES_URLS: str = [],
    MAX_CURRENT_INDEX_SIZE_GB: int = 50,
    MAX_RELOCATING: int = 25,
    MAX_TASKS: int = 500,
    MASTER_TIMEOUT: str = '2m',
    index_pattern: str = re.compile(r'^(shrink-)?(.+)-(\d{6})$'),
    index_pools: str = '',
    alias_list: str = '',
    settings_list: str = '',
    ilm_list: str = ''
  ):
    self.ELASTIC_URL = ELASTIC_URL
    self.ES_URLS: str = [
      "{0}/_cat/indices?format=json&bytes=gb".format(self.ELASTIC_URL),
      "{0}/_alias".format(self.ELASTIC_URL),
      "{0}/*/_settings".format(self.ELASTIC_URL),
      "{0}/*/_ilm/explain".format(self.ELASTIC_URL),
    ]
    self.MAX_CURRENT_INDEX_SIZE_GB = MAX_CURRENT_INDEX_SIZE_GB
    self.MAX_RELOCATING = MAX_RELOCATING
    self.MAX_TASKS = MAX_TASKS
    self.MASTER_TIMEOUT = MASTER_TIMEOUT
    self.index_pattern = index_pattern
    self.index_pools = index_pools
    self.alias_list = alias_list
    self.settings_list = settings_list
    self.ilm_list = ilm_list

if __name__ == "__main__":
  print(Config().ELASTIC_URL)
