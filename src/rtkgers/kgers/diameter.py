"""
See class summary.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
from Queue import PriorityQueue

import rtkgers.utils.math as MathUtils
import rtkgers.utils.hyperplane as HyperplaneUtils

from rtkgers.exthread import ExThread
from rtkgers.hyperplane import Hyperplane
from rtkgers.kgers.core import KGERSCore

from rtkgers.exceptions.hyperplane import HyperplaneException


class KGERSDiameter(KGERSCore):
  """
  The diameter KGERS algorithm takes the top X percent of the hyperplanes
  generated ranked by their respective diameter between points.
  """

  def execute(self):
    """See parent class summary."""

    num_of_hyperplanes = self.config.getint('KGERS', 'K') * \
      self.config.getint('KGERSDiameter', 'Multiple')

    workers = []
    for i in range(0, num_of_hyperplanes):
      worker = KGERSDiameter.Worker(i, self.training)
      worker.start()
      workers.append(worker)

    # Wait for all threads to complete.
    #  If an exception occurs, catch only the latest one
    #  and make sure all the threads finish out.
    queue = PriorityQueue()
    exception = None
    for worker in workers:
      try:
        worker.join_with_exception()
        # Insert the result into the queue, with the higher weights in front.
        queue.put((1.0 / worker.diameter, (worker.hyperplane, worker.weight)))
      except Exception, ex:
        exception = ex

    # If there was an exception in any of the threads,
    #  re-throw the latest one.
    if exception:
      raise exception

    hyperplanes = []
    weights = []
    for i in range(0, self.config.getint('KGERS', 'K')):
      hyperplane, weight = queue.get()[1]
      hyperplanes.append(hyperplane)
      weights.append(weight)

    self.coefficients = HyperplaneUtils.average(hyperplanes, weights)


  class Worker(ExThread):
    """The worker thread for the container class."""


    def __init__(self, uid, training):
      """
      Constructor.

      Key arguments:
      uid      -- The unique ID of the thread.
      training -- The training set to use for this thread.
      """

      ExThread.__init__(self)
      self.uid = uid
      self.training = training
      self.hyperplane = None
      self.weight = None
      self.diameter = 0.0


    def run_with_exception(self):
      """Generates a hyperplane and determines the weight."""

      # Create a hyperplane from the training points.
      hyperplane = Hyperplane.sample(self.training)

      # Grab a set of validators that are not in the training set.
      validators = MathUtils.sample(
        self.training,
        self.training[0].dimensions, # The number of point to sample is the dim.
        exclude=hyperplane.points)

      self.hyperplane = hyperplane

      # Find the weight for this hyperplane.
      self.weight = HyperplaneUtils.weigh(hyperplane, validators)

      # Find the diameter based on the distance between each segment.
      size = len(hyperplane.points)
      for i in range(0, size):
        point1 = hyperplane.points[i]
        point2 = hyperplane.points[(i + 1) % size]
        self.diameter += point1.distance(point2)
