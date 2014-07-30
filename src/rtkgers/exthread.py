"""
See class summary.

This implementation was originally found on stackoverflow at:
http://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import sys
import threading
import Queue


class ExThread(threading.Thread):
  """
  A thread class that is able to bubble up exceptions.
  """


  # The max number of threads to run at one time.
  Thread_Limit = threading.BoundedSemaphore(4)


  def __init__(self):
    """Constructor."""

    threading.Thread.__init__(self)
    self.__status_queue = Queue.Queue()


  def run_with_exception(self):
    """This method should be overriden."""

    raise NotImplementedError


  def run(self):
    """This method should NOT be overriden."""

    # Check the max thread limit first.
    ExThread.Thread_Limit.acquire()
    try:
      self.run_with_exception()
      self.__status_queue.put(None)
    except Exception:
      self.__status_queue.put(sys.exc_info())
    finally:
      ExThread.Thread_Limit.release()


  def wait_for_exc_info(self):
    """Returns the top level execution info (exception, if one occurred)."""

    return self.__status_queue.get()


  def join_with_exception(self):
    """Waits for this thread and raises an exception, if necessary."""

    ex_info = self.wait_for_exc_info()
    if ex_info is None:
      return
    else:
      raise ex_info[1]
