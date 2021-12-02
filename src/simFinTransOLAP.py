import logging
import os
import phoenixdb
import phoenixdb.cursor
import pytz
import warnings
from dataclasses import dataclass, field
from datetime import datetime
from time import sleep
from typing import List
from typing_extensions import Protocol, TypedDict

warnings.filterwarnings("ignore")

class FinTransDb(Protocol):
  def query(self) -> List[TypedDict]:
    ...

@dataclass
class FinTransHBaseDb(FinTransDb):
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

  def query(self) -> List[TypedDict]:
    """ Receives financial transactions from Hbase """
    with self.dbConn.cursor() as cur:
      cur.execute(
       """
        SELECT atm, SUM(amount) as total_withdrawals
        FROM DEMO_ATM_TRANS_ 
        WHERE UPPER(atm) LIKE 'WELLS FARGO' OR UPPER(atm) LIKE 'BANK OF AMERICA'
        GROUP BY atm
       """
      )
      results = cur.fetchall()

      tzNY = pytz.timezone('America/New_York') 
      print("As of today at {0}".format(datetime.now(tzNY).strftime("%H:%M:%S")))
      for _ in map(print, results):
        pass
      print("\n")

    return [{}]

  def close(self):
    self.dbConn.close()

if __name__ == '__main__':
# Build an Hbase Db source
  SIM_TARGET_HBASE_DB_URL = os.environ.get("SIM_TARGET_HBASE_DB_URL", "localhost:8756")
  SIM_TARGET_HBASE_AUTHN = os.environ.get("SIM_TARGET_HBASE_AUTHN", "SPNEGO")
  SIM_TARGET_HBASE_AUTO_COMMIT = os.environ.get("SIM_TARGET_HBASE_AUTO_COMMIT", "True")
  SIM_TARGET_HBASE_AUTO_COMMIT = True if SIM_TARGET_HBASE_AUTO_COMMIT=="True" else False
  SIM_TARGET_HBASE_SSL_VERIFY = os.environ.get("SIM_TARGET_HBASE_SSL_VERIFY", "False")
  SIM_TARGET_HBASE_SSL_VERIFY = True if SIM_TARGET_HBASE_SSL_VERIFY=="True" else False

  db = FinTransHBaseDb(
    authentication=SIM_TARGET_HBASE_AUTHN,
    autocommit=bool(SIM_TARGET_HBASE_AUTO_COMMIT),
    url=SIM_TARGET_HBASE_DB_URL,
    verify=bool(SIM_TARGET_HBASE_SSL_VERIFY))

  try:
    while True:
      db.query()
      sleep(10)

  finally:
    db.close()


