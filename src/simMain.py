""" 
  The main script to invoke the generator for synthetic streams 
"""

import logging
import os
from simFinTrans import FinTransSource

FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')

if __name__ == '__main__':

  SIM_DATA_FILE = os.environ.get("SIM_DATA_FILE")
  if SIM_DATA_FILE is None:
    SIM_DATA_FILE = "{0}/{1}".format(os.environ["SIM_HOME"], "data/sf-bay-area.csv")

  SIM_TARGET_UDP_PORT = os.environ.get("SIM_TARGET_UDP_PORT")
  if SIM_TARGET_UDP_PORT is None:
    logging.debug("bitch")
    SIM_TARGET_UDP_PORT = 6900
  else:
    SIM_TARGET_UDP_PORT = int(SIM_TARGET_UDP_PORT)

  # defines delay (seconds) to inject between events
  SIM_EVENT_DELAY = os.environ.get("SIM_EVENT_DELAY")
  if SIM_EVENT_DELAY is None:
    SIM_EVENT_DELAY = 0.75
  else:
    SIM_EVENT_DELAY=float(SIM_EVENT_DELAY)

  SIM_MAX_ACCOUNT_ID = os.environ.get("SIM_MAX_ACCOUNT_ID")
  if SIM_MAX_ACCOUNT_ID is None:
    SIM_MAX_ACCOUNT_ID = 1000
  else:
    SIM_MAX_ACCOUNT_ID=int(SIM_MAX_ACCOUNT_ID)

  # specify a default timezone
  SIM_TIMEZONE = os.environ.get("SIM_TIMEZONE")
  if SIM_TIMEZONE is None:
    SIM_TIMEZONE = "US/Pacific"

  fns = FinTransSource(atmDataInput=SIM_DATA_FILE, 
                       targetUDPPort=SIM_TARGET_UDP_PORT,
                       eventDelay=SIM_EVENT_DELAY,
                       timezone=SIM_TIMEZONE)
  logging.info(FinTransSource.__doc__)
  fns.loadData()
  fns.run()


