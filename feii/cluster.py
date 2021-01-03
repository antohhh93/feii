#!/usr/bin/python3

import requests
from feii.config import Config

class Cluster(Config):
  def __init__(self,
    cluster: str = {},
  ):
    super().__init__()
    self.cluster = cluster

  def get_status_cluster(self):
    self.cluster = requests.get("{0}/_cluster/health".format( self.ELASTIC_URL )).json()

  def check_status_cluster_not_red(self):
    return self.cluster['status'] != "red"

  def check_count_relocating_shards_in_cluster(self):
    return int(self.cluster['relocating_shards']) <= self.MAX_RELOCATING

  def check_count_pending_tasks_in_cluster(self):
    return int(self.cluster['number_of_pending_tasks']) <= self.MAX_TASKS

  def retry_failed(self):
    return requests.post("{0}/_cluster/reroute?retry_failed".format( self.ELASTIC_URL ))

if __name__ == "__main__":
  class_cluster = Cluster()
  class_cluster.get_status_cluster()

  if class_cluster.check_status_cluster_not_red():
    print('not red')
  if class_cluster.check_count_relocating_shards_in_cluster():
    print('ok relocating_shards')
  if class_cluster.check_count_pending_tasks_in_cluster():
    print('ok pending_tasks')
  print(class_cluster.cluster)
