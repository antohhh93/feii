#!/usr/bin/python3

import re
import requests
from multiprocessing.dummy import Pool as ThreadPool
from feii.config import Config

class Init(Config):
  def __init__(self,
    count: int = 1,
  ):
    super().__init__()
    self.count = count

  def list_pools(self):
    pool = ThreadPool(int(self.count))
    results = pool.map(requests.get, self.ES_URLS)
    pool.close()
    return results

if __name__ == "__main__":
  Init(count = 4).list_pools()
  class_config = Config
  class_config.index_pools = Init(count = 4).list_pools()
  class_config.alias_list = class_config.index_pools[1].json()
  class_config.settings_list = class_config.index_pools[2].json()
  class_config.ilm_list = class_config.index_pools[3].json()
