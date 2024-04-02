""" 
  The main script to invoke the generator for synthetic streams 
"""

import logging
import os
from simFinTrans import FinTransSource
from simFinTransReceiver import FinTransUDPReceiver

FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')

if __name__ == '__main__':

  SIM_DATA_FILE = os.environ.get("SIM_DATA_FILE")
  if SIM_DATA_FILE is None:
    SIM_DATA_FILE = "{0}/{1}".format(os.environ["SIM_HOME"], "data/sf-bay-area.csv")

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

  SIM_TARGET_RECEIVER = os.environ.get("SIM_TARGET_RECEIVER")
  # Build a UDP Receiver
  if SIM_TARGET_RECEIVER.upper() == "UDP":
    SIM_TARGET_UDP_PORT = os.environ.get("SIM_TARGET_UDP_PORT")
    if SIM_TARGET_UDP_PORT is None:
      SIM_TARGET_UDP_PORT = 6900
    else:
      SIM_TARGET_UDP_PORT = int(SIM_TARGET_UDP_PORT)

    SIM_TARGET_UDP_HOST = os.environ.get("SIM_TARGET_UDP_HOST", "localhost")
    SIM_TARGET_RECEIVER = FinTransUDPReceiver(host=SIM_TARGET_UDP_HOST, port=SIM_TARGET_UDP_PORT)

  else:
    SIM_TARGET_RECEIVER = FinTransUDPReceiver(host="localhost", port=6900)

  fns = FinTransSource(atmDataInput=SIM_DATA_FILE, 
                       eventDelay=SIM_EVENT_DELAY,
                       timezone=SIM_TIMEZONE,
                       receiver=SIM_TARGET_RECEIVER)
  logging.info(FinTransSource.__doc__)
  fns.loadData()
  fns.run()


