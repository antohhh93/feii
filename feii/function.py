#!/usr/bin/python3

import re
import time
from feii.log import Log

class Function:
  def __init__(self,
    next_index: str = '',
    prev_index: str = '',
    retry: int = 0,
  ):
    super().__init__()
    self.next_index = next_index
    self.prev_index = prev_index
    self.retry = retry

  def debug_detail_index(self):
    self.index = 'test-000001'
    self.retry = 1

  def find_next_index(self):
    alias = self.index[:-6]
    number = self.index[-6:]
    self.next_index = alias + str('{:06}'.format(int(number) + 1))
    return self.next_index

  def find_prev_index(self):
    alias = self.index[:-6]
    number = self.index[-6:]
    self.prev_index = alias + str('{:06}'.format(int(number) - 1))
    return self.prev_index

  def time_sleep(self):
    if self.retry > 0:
      self.logger.warning("Sleep time {0}".format( int(60 * self.retry) ))
      time.sleep(60 * self.retry)

if __name__ == "__main__":
  class_log = Log()
  class_log.remove_old_log_file()
  class_log.get_file_handler()
  class_log.get_stream_handler()
  class_log.get_logger()

  class_function = Function()
  class_function.debug_detail_index()

  class_function.logger = class_log.logger

  class_function.find_next_index()
  class_function.find_prev_index()
  class_function.time_sleep()
