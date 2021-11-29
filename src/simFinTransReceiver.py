import logging
import socket
from typing import Protocol

class FinTransReceiver(Protocol):
  def send(self, finTranJSON: str) -> None:
    ...

class FinTransUDPReceiver(FinTransReceiver):
  def __init__(self, host: str, port: int):
    self.host = host
    self.port = port
    self.sOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def send(self, finTranJSON: str) -> None:
    """ Sends a single financial transaction via UDP """
    self.sOut.sendto(finTranJSON.encode(), (self.host, self.port))
    logging.debug("Sent financial transaction: {0} to port {1} at {2}".format(finTranJSON, self.port, self.host))


