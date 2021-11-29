import csv
import datetime
import json
import logging
import os
import random
import sys
import uuid
from dataclasses import dataclass, field
from pytz import timezone
from simFinTransReceiver import FinTransReceiver
from time import sleep
from typing import List

FORMAT = "%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]"
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="%Y-%m-%dT%I:%M:%S")

@dataclass
class FinTransModel:
  minWithdrawal: int = 40
  maxWithdrawal: int = 600
  increments: int = 20
  maxNumAccounts: int = 1000
  fraudTickMin: int = 5
  fraudTickMax: int = 15
  withdrawalAmounts: List[int] = field(init=False, repr=False, default_factory=lambda: [0])

  def __post_init__(self):
    self.withdrawlAmounts = list(range(self.minWithdrawal, self.maxWithdrawal, self.increments))

@dataclass
class FinTransSource:
  """ 
    The implementation of the synthetic financial transaction stream used by the main script
  """
  _atmLoc = {}

  atmDataInput: str 
  eventDelay: int
  timezone: str
  receiver: FinTransReceiver
  model: FinTransModel = FinTransModel()

  def loadData(self) -> None:
    """  Loads the ATM location data from the specified CSV data file """
    logging.info("Trying to parse ATM location data file %s" %(self.atmDataInput))
    osmAtmFile = open(self.atmDataInput, "r")
    i= 0
    try:
      reader = csv.reader(osmAtmFile, delimiter=",")
      for row in reader:
        lat, lon, atmLabel = row[1], row[0], row[2] 
        i += 1
        self._atmLoc[str(i)] = lat, lon, atmLabel
        logging.debug(" -> loaded ATM location %s, %s" %(lat, lon))

    finally:
      osmAtmFile.close()
      logging.debug(" -> loaded %d ATM locations in total." %(i))
  
  def createFinTran(self) -> {}:
    """
      Obtains a random ATM location
      Simulates an account id (1-1000) and a transaction id (uniquely)
      Randomly picks a withdrawal amount from predefined self.model.withdrawalAmounts list
    """
    rloc = random.choice(list(self._atmLoc.keys())) 
    lat, lon, atmLabel = self._atmLoc[rloc]
    loc_dt = datetime.datetime.now(timezone(self.timezone))
    finTran = {
      "timestamp" : str(loc_dt.strftime("%Y-%m-%d %H:%M:%S %z+0000")),
      "atm" : str(atmLabel),
      "location" : {
        "lat" : str(lat),
        "lon" :  str(lon)
      },
      "amount" : random.choice(self.model.withdrawalAmounts),
      "account_id" : "a" + str(random.randint(1, self.model.maxNumAccounts)),
      "transaction_id" : str(uuid.uuid1())
    }    
    logging.debug("Created financial transaction: %s" %finTran)
    return finTran

  def createFraudTran(self, finTran: {}) -> {}:
    """ Creates a fraudulent transaction """
    rloc = random.choice(list(self._atmLoc.keys())) # obtain a random ATM location
    lat, lon, atmLabel = self._atmLoc[rloc]
    loc_dt = (datetime.datetime.now(timezone(self.timezone)) - datetime.timedelta(seconds=random.randint(60,600)))
    fraudTran = {
      "timestamp" : loc_dt.strftime("%Y-%m-%d %H:%M:%S %z+0000"),
      "atm" : str(atmLabel),
      "location" : {
        "lat" : str(lat),
        "lon" : str(lon)
      },
      "amount" : random.choice(self.model.withdrawalAmounts),
      "account_id" : finTran["account_id"],
      # Tag the fraudulent transaction
      "transaction_id" : "xxx" + str(finTran["transaction_id"])
    }    
    logging.debug("Created fraudulent financial transaction: %s" %fraudTran)
    return fraudTran

  def sendFinTran(self, finTranJSON: str) -> None:
    self.receiver.send(finTranJSON) 
    
  def dumpData(self) -> None:
    """ Dump the geocoded ATM dataset """
    for k, v in self._atmLoc.iteritems():
      logging.info("ATM %s location: %s %s" %(k, v[0], v[1])) 
  
  def run(self) -> None:
    """ Generates financial transactions (ATM withdrawals) and sends them to a UDP port """
    ticks = 0 
    fraudTick = random.randint(self.model.fraudTickMin, self.model.fraudTickMax) 

    logging.info("Sim is running")

    while True:
      ticks += 1      
      logging.debug("TICKS: %d" %ticks)
      finTran = self.createFinTran()
      self.sendFinTran(json.dumps(finTran))

      sleep(self.eventDelay)

      # A fraudulent transaction will be created according to a randomized number of TICKS * DELAY in seconds 
      if ticks > fraudTick:
        fraudTran = self.createFraudTran(finTran)
        self.sendFinTran(json.dumps(fraudTran))
        ticks = 0
        fraudTick = random.randint(self.model.fraudTickMin, self.model.fraudTickMax)
