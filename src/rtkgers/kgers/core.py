"""
Test the point class.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import abc
import math
import random

import rtkgers.utils.math as MathUtils

from rtkgers.hyperplane import Hyperplane

from rtkgers.exceptions.kgers import KGERSException



class KGERSCore(object):
  """
  The KGERS core class contains methods that pertain to all extensions,
  e.g. finding the error based on the test set.
  """
  __metaclass__ = abc.ABCMeta


  def __init__(self, config, points, test = None):
    """
    Contructor.

    Key arguments:
    points -- The points to train on.
    test   -- The points to test against. If this is not provided,
    approximately 30 percent of the points provided will be used
    for test.
    """

    # Save the configuration.
    self.config = config

    # Make sure we have more than one point.
    if (len(points) == 0):
      raise KGERSException("Not enough points provided.")

    # If a test set was provided, we only need 2 * (n + 1) points.
    if (test != None and len(points) < 2 * (points[0].dimensions)):
      raise KGERSException("Not enough points to train on.")

    # The test set needs to be generated here, we need at least 3 * (n + 1).
    if (test == None and len(points) < 3 * (points[0].dimensions)):
      raise KGERSException("Not enough points to train on.")

    # Check if we need to generate the test set.
    if (test == None):
      # Take 30% of the data set for testing, or the minimum required.
      num_of_test = max([int(len(points) * .3), points[0].dimensions])
      test = MathUtils.sample(points, size=num_of_test)

    # Set the test set.
    self.test = test
    # The training is all the points remaining minus the test set.
    self.training = list(set(points).difference(set(self.test)))


  def error(self, test = None):
    """
    Returns the RMSE of the hyperplane based on the test set.

    Key arguments:
    test -- The test set to test against. If one is not provided, the test set
    saved in the beginning will be used.
    """

    if (test == None):
      test = self.test

    return math.sqrt(
      sum([pow(self.solve(point) - point.solution, 2) for point in test]) /
      float(len(test)))


  @abc.abstractmethod
  def execute(self):
    """
    Executes the primary algorithm that generates the approximate
    hyperplane for the points.
    """
    return


  def solve(self, point):
    """
    Determines the solution of the point using the
    linear equation of the hyperplane.

    Key arguments:
    point -- The point to solve for.
    """

    return sum([a * b for a, b in zip(self.coefficients[:-1], point.features)]) \
      + self.coefficients[-1]
