"""
See class summary.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import util

from core import KGERSCore
from hyperplane import Hyperplane
from exceptions.hyperplane import HyperplaneException


class KGERSOriginal(KGERSCore):
  """
  """

  def execute(self):
    """
    """

    self.hyperplanes = []
    self.weights = []

    for i in range(0, 10):
      # Create a hyperplane from the training points.
      hyperplane = Hyperplane.sample(self.training)

      # Grab a set of validators that are not in the training set.
      validation = util.sample(self.training, exclude=hyperplane.points)

      self.hyperplanes.append(hyperplane)

      # Find the weight for this hyperplane.
      self.weights.append(self.weigh(hyperplane, validators))

    self.coefficients = self.average(self.hyperplanes, self.weights)
