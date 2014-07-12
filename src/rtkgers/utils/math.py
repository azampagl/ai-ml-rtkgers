"""
Math related utility methods.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import random


def sample(points, size, exclude = []):
  """
  Samples a set of points and returns a list.

  Key arguments:
  points  -- The set of points to sample from.
  size    -- The number of points to return.
  exclude -- The set of points to NOT include.
  """

  # Take a random sampling, but do not include the excluded group.
  return list(random.sample(set(points).difference(set(exclude)), size))
