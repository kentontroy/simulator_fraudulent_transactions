#!/bin/bash -

################################################################################
# Test the simulator by outputting to netcat
# Usage: 
#
# ${SIM_HOME}/scripts/sim.sh
# ${SIM_HOME}/scripts/simTestNetCat.sh
#
#
nc -v -u -l ${SIM_TARGET_UDP_PORT} | tee ${SIM_HOME}/logs/simTestNetCat.log
