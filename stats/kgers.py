"""
Main execution script for kgers.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import csv
import getopt
import math
import os
import sys
import threading
import timeit

import ConfigParser

from rtkgers.exthread import ExThread
from rtkgers.hyperplane import Hyperplane
from rtkgers.point import Point
from rtkgers.kgers.original import KGERSOriginal
from rtkgers.kgers.weights import KGERSWeights


def main():
  """Main execution."""

  # Determine command line arguments.
  try:
    rawopts, _ = getopt.getopt(sys.argv[1:], 'c:s:i:o:')
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  opts = {}

  # Process each command line argument.
  for o, a in rawopts:
    opts[o[1]] = a

  # The following arguments are required in all cases.
  for opt in ['c', 's', 'i', 'o']:
    if not opt in opts:
      usage()
      sys.exit(2)

  # Load in the configuration.
  config = ConfigParser.ConfigParser()
  config.read(opts['c'])

  # Load in the stat settings.
  settings = ConfigParser.ConfigParser()
  settings.read(opts['s'])

  # The points are essentially feature sets with the known solution.
  points = []

  # Create our reader.
  with open(opts['i'], 'rb') as reader_file:
    reader = csv.reader(reader_file, delimiter=',', quotechar='|')

    # Skip the first line.
    reader.next()
    for row in reader:
      points.append(
        Point([float(feature) for feature in row[2:]], float(row[1])))

  # Overload globals.
  max_threads = config.getint('Main', 'MaxThreads')
  max_sample_attempts = config.get('KGERS', 'MaxHyperplaneAttempts')
  ExThread.Thread_Limit = threading.BoundedSemaphore(max_threads)
  Hyperplane.MAX_SAMPLE_ATTEMPTS = max_sample_attempts

  # Load the desired algorithm.
  algorithm = config.get('KGERS', 'Algorithm')

  # Maintain a list of actual errors and times.
  errors = []
  times = []

  # Maintain a count of rounded errors and times.
  rounded_errors = {}
  rounded_times = {}

  for i in range(settings.getint('Stats', 'NumOfTrials')):
    # Construct the desired KGERS implementation.
    kgers = globals()[algorithm](config, points)

    # Execute.
    timer = timeit.Timer(lambda: kgers.execute())
    time = timer.timeit(1)
    error = kgers.error()

    # Append to the an actual list.
    errors.append(error)
    times.append(time)

    # Add to the rounded error list.
    rounded_error = str(round(error, settings.getint('Stats', 'ErrorSigFig')))
    if rounded_error in rounded_errors:
      rounded_errors[rounded_error] += 1
    else:
      rounded_errors[rounded_error] = 1

    # Add to the rounded time list.
    rounded_time = str(round(time, settings.getint('Stats', 'TimeSigFig')))
    if rounded_time in rounded_times:
      rounded_times[rounded_time] += 1
    else:
      rounded_times[rounded_time] = 1

  error_sigfig = pow(10, settings.getint('Stats', 'ErrorSigFig'))
  error_display_min = settings.getfloat('Stats', 'MinErrorDisplay')
  error_display_max = settings.getfloat('Stats', 'MaxErrorDisplay')

  time_sigfig = pow(10, settings.getint('Stats', 'TimeSigFig'))
  time_display_min = settings.getfloat('Stats', 'MinTimeDisplay')
  time_display_max = settings.getfloat('Stats', 'MaxTimeDisplay')

  # Write to the output file.
  with open(opts['o'], 'w') as writer:

    # Write the RMSE.
    writer.write("RMSE\tCount\n")

    error = error_display_min
    while error < error_display_max:
      if str(error) in rounded_errors:
        writer.write(str(error) + "\t" + str(rounded_errors[str(error)]) + "\n")
      else:
        writer.write(str(error) + "\t" + str(0) + "\n")

      error = round(
        error + 1.0 / error_sigfig,
        settings.getint('Stats', 'ErrorSigFig'))

    # Final stats, avg, stdev, etc.
    avg = sum(errors) / float(len(errors))
    stdev = math.sqrt(sum([math.pow(e - avg, 2) for e in errors]) / float(len(errors)))
    writer.write("Average:\t" + str(avg) + "\n")
    writer.write("Stdev:\t" + str(stdev) + "\n")

    # Write the Time.
    writer.write("\nTime\tCount\n")

    time = time_display_min
    while time < time_display_max:
      if str(time) in rounded_times:
        writer.write(str(time) + "\t" + str(rounded_times[str(time)]) + "\n")
      else:
        writer.write(str(time) + "\t" + str(0) + "\n")

      time = round(
        time + 1.0 / time_sigfig,
        settings.getint('Stats', 'TimeSigFig'))

    # Final stats, avg, stdev, etc.
    avg = sum(times) / float(len(times))
    stdev = math.sqrt(sum([math.pow(t - avg, 2) for t in times]) / float(len(times)))
    writer.write("Average:\t" + str(avg) + "\n")
    writer.write("Stdev:\t" + str(stdev) + "\n")

def usage():
  """Prints the usage of the program."""

  print("\n" +
    "The following are arguments required:\n" +
    "\t-c: the path to the configuration file.\n" +
    "\t-t: the number of trials.\n" +
    "\t-i: the input file.\n" +
    "\n" +
    "Example Usage:\n" +
    "\tpython kgers.py -c \"config.cfg\" -i \"training.csv\"" +
    "\n")


"""Main execution."""
if __name__ == "__main__":
  main()
