```
Goal is to simulate financial transactions (ATM withdrawal) in the following
format:
{   
  "account_id": "a228",
  "timestamp": "2018-10-05T10:47:54.189407",
  "atm": "Bank of the West",
  "amount": 300,
  "location": {
     lat: "37.2500148",
     lon: "-121.8621345"
  },
  "transaction_id": "bb35284a-c883-11e8-8421-186590d22a35"
}
```

```
Extending ATM locations

If you want to add new ATM locations, then you need to do the following:

1. Choose a geographic area and download the respective `.osm` dump from sites such as 
    * https://export.hotosm.org/en/v3/
        * (e.g. https://export.hotosm.org/en/v3/exports/7e60635f-18b4-4650-9146-68c72a3a6c65)
        * From HOTOSM you can opt to download _just_ ATM points, which makes the file smaller
    * https://archive.org/download/metro.teczno.com
    * https://osmaxx.hsr.ch/
1. Then, run `data/extract_atms.py`, which uses the ATM-tagged nodes in [OSM/XML](http://wiki.openstreetmap.org/wiki/OSM_XML) format and extracts/converts it into the [CSV format](data/osm-atm-garmin.csv) used internally, by gess.
1. You can also download KML format data and use the `extract_atms_kml.py` script (`pykml` was an easier library to install than the `imposm` library required for OSM)
1. Add the generated ATM location data file in CSV format to `gess.conf` so that gess picks it up on startup time.
```

