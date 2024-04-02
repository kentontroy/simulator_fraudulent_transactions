sh -c './sim.sh start && nc -u -l 6901 | ./kafka/bin/kafka-console-producer.sh --topic demo_atm_trans --bootstrap-server 192.168.144.6:9092'
