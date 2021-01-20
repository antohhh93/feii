#!/usr/bin/python3

import os
from configparser import ConfigParser
from feii.config import Config

class PathToFile(Config):
  def __init__(self,
  ):
    super().__init__()

  def get_config(self):
    config_file = ConfigParser()
    config_file.read(self.path)
    self.t1 = config_file

    if config_file.has_option("CONFIG", "elastic_url"):
      Config.ELASTIC_URL = config_file.get("CONFIG", "elastic_url")

if __name__ == "__main__":

  class_path_to_file = PathToFile()
  class_path_to_file.get_config(path)
