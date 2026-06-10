#!/bin/bash

for i in $(seq 1 1000); do
  #agentarts invoke '{"message": "hello,world"}' --session haolipeng &
  nohup agentcore invoke --runtime awsagent  hello & #--session-id 0cf0f627-baee-4e36-a302-b7f58e44da9c &
  if (( i % 10 == 0 )); then
    wait
  fi
done
wait
