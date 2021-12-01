import json
import logging
import phoenixdb
import phoenixdb.cursor
import socket
from dataclasses import dataclass, field
from typing_extensions import Protocol

class FinTransReceiver(Protocol):
  def send(self, finTran: {}) -> None:
    ...

class FinTransUDPReceiver(FinTransReceiver):
  def __init__(self, host: str, port: int):
    self.host = host
    self.port = port
    self.sOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def send(self, finTran: {}) -> None:
    """ Sends a single financial transaction via UDP """
    finTranJSON = json.dumps(finTran)
    self.sOut.sendto((finTranJSON + "\n").encode(), (self.host, self.port))
    logging.debug("Sent financial transaction: {0} to port {1} at {2}".format(finTranJSON, self.port, self.host))

@dataclass
class FinTransHBaseReceiver(FinTransReceiver):
  url: str
  authentication: str = "SPNEGO"
  autocommit: bool = True
  verify: bool = False 
  dbConn: phoenixdb.connection.Connection = field(init=False, repr=False, default=None)

  def __post_init__(self):
    self.dbConn = phoenixdb.connect(
      url = self.url, 
      autocommit = self.autocommit, 
      verify = self.verify, 
      authentication = self.authentication)

  def send(self, finTran: {}) -> None:
    """ Sends a single financial transaction to Hbase """
    cur = self.dbConn.cursor()
    cur.execute(
      """
      UPSERT INTO DEMO_ATM_TRANS_ (transaction_id, account_id, timestamp, atm, lat, lon, amount)
      VALUES (?, ?, ?, ?, ?, ?, ?) 
      """,
      (finTran["transaction_id"], finTran["account_id"], finTran["timestamp"], 
       finTran["atm"], finTran["location"]["lat"], finTran["location"]["lon"], 
       finTran["amount"])
    )
    logging.debug("Sent financial transaction to Hbase: {0}".format(finTran))

