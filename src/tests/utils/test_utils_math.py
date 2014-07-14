"""
Test the math utility methods.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
from rtkgers.utils.math import sample


def test_sample_simple():
  """Test the sample method by sampling from a simple population."""

  # Make a population to sample from.
  population = [1, 2, 3]

  # Sample a bunch of trials and make sure the sample exists
  #  in the population.
  for i in range (0, 100):
    samples = sample(population, 1)
    assert samples[0] in population


def test_sample_exlude():
  """
  Test the sample method by sampling from a simple population
  and making sure the exluding item is not in the sample list.
  """

  # Make a population to sample from.
  population = [1, 2, 3, 4, 5]

  # Sample a bunch of trials and make sure the sample exists
  #  in the population.
  for i in range (0, 100):
    samples = sample(population, 2, [3])
    assert not 3 in samples
