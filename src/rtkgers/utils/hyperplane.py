"""
Hyperplane related utility methods.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import numpy as np
import sys

from rtkgers.point import Point


def average(hyperplanes, weights):
  """
  Averages all of the hyperplanes together with their respective weights.

  Key arguments:
  hyperplanes -- The hyperplanes to average.
  weights     -- The respective weights for each hyperplane.
  """

  # Find if there is a "perfect" hyperplane in the list
  #  by looking for a max weight.
  try:

    index = weights.index(sys.float_info.max)

    return hyperplanes[index].coefficients

  except ValueError:
    # Do nothing and continue.
    pass

  # Find the total weight
  total_weight = sum(weights)

  # Find the length of the hyperplane coefficients.
  hyperplane_len = len(hyperplanes[0].coefficients)
  # Initialize coefficients to 0.
  coefficients = np.array([0.0] * hyperplane_len, dtype=Point.DTYPE)

  for i in range(0, len(hyperplanes)):
    hyperplane = hyperplanes[i]
    hyperplane_weight = weights[i] / total_weight

    for j in range(0, hyperplane_len):
      coefficients[j] += hyperplane.coefficients[j] * hyperplane_weight

  return coefficients


def weigh(hyperplane, validators):
  """
  Determine the weight of a hyperplane based on a set of validators.

  If the hyperplane is a perfect fit for the validators, this method
  will return -1.0.

  Otherwise, a fraction is returned. The smaller the fraction, the less
  accurate the hyperplane was in regards to the provided validators.

  Key arguments:
  hyperplane -- The hyperplane to determine the weight for.
  validators -- The set of points to validate against the hyperplane.
  """

  summation = sum([pow(hyperplane.solve(validator) - validator.solution, 2)
    for validator in validators])

  # If the summation was 0, that means the hyperplane was a perfect fit for
  #  the validators.
  if round(summation, 5) == 0.0:
    return sys.float_info.max

  return 1.0 / summation
