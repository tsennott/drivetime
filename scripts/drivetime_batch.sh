#!/bin/bash

# command to kill background processes on exit
trap 'kill -9 $PID_1 $PID_2' EXIT

ADDRESS_1="264 Lee St, Oakland CA"
ADDRESS_2="3542 Bassett St, Santa Clara CA"

python drivetime_cli.py "$ADDRESS_1" "$ADDRESS_2" --filepath out_1.csv --interval 5 &
PID_1=$!

python drivetime_cli.py "$ADDRESS_2" "$ADDRESS_1" --filepath out_2.csv --interval 5 &
PID_2=$!

wait
