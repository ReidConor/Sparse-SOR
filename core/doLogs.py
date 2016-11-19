import os
import logging


def writeToLogs (stoppingReason, outputFile):
    fn = os.path.join(os.path.dirname(__file__), outputFile)
    logging.basicConfig(filename=fn, filemode='w', level=logging.DEBUG)

    logging.info('Stopping reason  Max num of iterations  Number of iterations Machine epsilon  X seq tolerance ')
    logging.info("%s %d %d %s %s " % (stoppingReason, 2, 2, "blah", "blah"))
