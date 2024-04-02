#!/bin/bash -

################################################################################
# This is the script that allows you to start or stop sim.
# Usage: ./sim.sh start | stop | status

SIM_LOG=${SIM_HOME}/logs/sim.log
SIM_PID=sim.pid

function usage() {
  printf "Usage: %s start | stop | test\n" $0
}

function start_sim() {
  nohup python3 ${SIM_HOME}/simMain.py &> $1 &
  echo $! > $SIM_PID
}

function test_mods() {
  nc -v -u -l ${SIM_TARGET_UDP_PORT} | tee ${SIM_HOME}/logs/simTestNetCat.log
}

function stop_sim() {
# try to find the PID of sim process and kill it
  if [ -f $SIM_PID ]; then
    if kill -0 `cat $SIM_PID` > /dev/null 2>&1; then
      echo 'Shutting down sim ...'
      kill `cat $SIM_PID`
      rm $SIM_PID
    fi
  fi
	
# ... as well as clean up the nohup stuff
  if [ -f nohup.out ]; then
    rm nohup.out
  fi
}

# main script
case $1 in
 start )  start_sim $SIM_LOG ;;
 stop )   stop_sim ;;
 test )   test_mods ;;
 * )      usage ; exit 1 ; ;;
esac
