```
First Kafka Broker:
tsantiago-pse-webinar-kafka-corebroker1.se-sandb.a465-9q4k.cloudera.site 

Master Node:
tsantiago-pse-webinar-kafka-master0.se-sandb.a465-9q4k.cloudera.site

cat kafka.properties

security.protocol=SASL_SSL
sasl.kerberos.service.name=kafka
sasl.mechanism=GSSAPI
sasl.jaas.config=com.sun.security.auth.module.Krb5LoginModule required \
  principal="kdavis@SE-SANDB.A465-9Q4K.CLOUDERA.SITE" \
  useTicketCache=true \
  serviceName="kafka";

kafka-topics --list --bootstrap-server tsantiago-pse-webinar-kafka-corebroker2.se-sandb.a465-9q4k.cloudera.site:9093 --command-config client.properties

kafka-topics --create --topic demo_atm_trans --partitions 1 --bootstrap-server tsantiago-pse-webinar-kafka-corebroker2.se-sandb.a465-9q4k.cloudera.site:9093 --command-config ${SIM_HOME}/conf/kafka.properties

source ${SIM_HOME}/scripts/sim.env

${SIM_HOME}/scripts/sim.sh start

${SIM_HOME}/scripts/simKafkaProducer.sh

kafka-console-consumer --from-beginning --topic demo_atm_trans --bootstrap-server tsantiago-pse-webinar-kafka-corebroker2.se-sandb.a465-9q4k.cloudera.site:9093 --consumer.config ${SIM_HOME}/conf/kafka.properties

```
