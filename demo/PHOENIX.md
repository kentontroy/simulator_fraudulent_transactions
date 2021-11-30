$ phoenix-sqlline

Setting property: [incremental, false]
Setting property: [isolation, TRANSACTION_READ_COMMITTED]
issuing: !connect -p driver org.apache.phoenix.jdbc.PhoenixDriver -p user "none" -p password "none" "jdbc:phoenix:"
Connecting to jdbc:phoenix:

0: jdbc:phoenix:> show tables;
+-----------+-------------+------------+--------------+---------+-----------+---------------------------+----------------+-------+
| TABLE_CAT | TABLE_SCHEM | TABLE_NAME |  TABLE_TYPE  | REMARKS | TYPE_NAME | SELF_REFERENCING_COL_NAME | REF_GENERATION | INDEX |
+-----------+-------------+------------+--------------+---------+-----------+---------------------------+----------------+-------+
|           | SYSTEM      | CATALOG    | SYSTEM TABLE |         |           |                           |                |       |
|           | SYSTEM      | CHILD_LINK | SYSTEM TABLE |         |           |                           |                |       |
|           | SYSTEM      | FUNCTION   | SYSTEM TABLE |         |           |                           |                |       |
|           | SYSTEM      | LOG        | SYSTEM TABLE |         |           |                           |                |       |
|           | SYSTEM      | MUTEX      | SYSTEM TABLE |         |           |                           |                |       |
|           | SYSTEM      | SEQUENCE   | SYSTEM TABLE |         |           |                           |                |       |
|           | SYSTEM      | STATS      | SYSTEM TABLE |         |           |                           |                |       |
|           | SYSTEM      | TASK       | SYSTEM TABLE |         |           |                           |                |       |
|           |             | USERS      | TABLE        |         |           |                           |                |       |
+-----------+-------------+------------+--------------+---------+-----------+---------------------------+----------------+-------+
