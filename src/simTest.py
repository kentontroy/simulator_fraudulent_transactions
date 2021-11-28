import datetime
import json
import os
import pytz
import random
import sys

def parseConfig():
  cf = os.path.abspath(os.environ["SIM_JOB_CONFIG_FILE"])
  if os.path.exists(cf):
    with open(cf) as f:
      params = json.load(f)

      try:
        m = params['map_overlay']
        atm_loc_source = os.path.abspath(m.strip())
      except KeyError:
        sys.exit("Missing map_overlay")

      try:
        tzone = params['timezone']
        if (tzone not in pytz.all_timezones):
          sys.exit("Invalid timezone")       

      except KeyError:
        sys.exit("Missing timezone")       

      try:
        tyear = int(params['start_year'])
        tmonth = int(params['start_month'])
        tdate = int(params['start_date'])
        config_date = datetime.date(tyear, tmonth, tdate) 

      except KeyError:
        sys.exit("Invalid calendar parameter")       

      except ValueError as e:
        sys.exit(str(e))
     
      return atm_loc_source, tzone, config_date
  else:
    sys.exit("Invalid JSON configuration")

def getRandomTimeFromStart(d):
  h = random.randint(0, 23)
  m = random.randint(0, 59)
  dt = datetime.datetime.combine(d, datetime.time(h, m))
  return dt

if __name__ == '__main__':
  atm_loc_source, tzone, config_date = parseConfig()
  print(config_date)
  print(getRandomTimeFromStart(config_date))
