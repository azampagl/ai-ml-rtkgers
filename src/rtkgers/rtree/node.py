"""
See class summary.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""

class Node(object):
  """Node class for the recursive tree."""

  def __init__(self):
    """Constructor."""

    # The feature analyzed at the time this node was generated.
    self.feature = None

    # The hyperplane (model) that represents this node.
    self.hyperplane = None
    self.index = 0

    # The left and right children of this node (optional).
    self.left = None
    self.right = None

    # The threshold that this node was split at.
    self.threshold = None
