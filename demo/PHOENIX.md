```
$ phoenix-sqlline

Setting property: [incremental, false]
Setting property: [isolation, TRANSACTION_READ_COMMITTED]
issuing: !connect -p driver org.apache.phoenix.jdbc.PhoenixDriver -p user "none" -p password "none" "jdbc:phoenix:"
Connecting to jdbc:phoenix:

0: jdbc:phoenix:> 
CREATE TABLE DEMO_ATM_TRANS
  (transaction_id VARCHAR PRIMARY KEY,
   account_id VARCHAR,
   timestamp VARCHAR,
   atm VARCHAR,
   lat VARCHAR,
   lon VARCHAR,
   amount INTEGER)
```
