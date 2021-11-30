nc -u -l ${SIM_TARGET_UDP_PORT} | kafka-console-producer --topic demo_atm_trans \
   --bootstrap-server tsantiago-pse-webinar-kafka-corebroker2.se-sandb.a465-9q4k.cloudera.site:9093 \
   --producer.config ${SIM_HOME}/conf/kafka.properties
