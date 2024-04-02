import json
import logging
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
