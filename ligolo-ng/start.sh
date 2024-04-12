#! /bin/bash

cp /app/agent /app/target/agent && \
cp /app/agent.exe /app/target/agent.exe && \
/app/proxy -selfcert "$@"
