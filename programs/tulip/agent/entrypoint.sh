#!bin/bash

# Backup /traffic/agentcapture.pcap and remove the file
mv /traffic/agentcapture.pcap "/traffic/agentcapture.pcap.$(date).bak" || echo "Couldn't create backup, probably new project"
touch /traffic/agentcapture.pcap
chmod 777 /traffic/agentcapture.pcap

echo $PRIVATE_KEY | base64 -d > ~/.ssh/agentkey
chmod 0600 ~/.ssh/agentkey

# Attempt to ssh to the target with the environment variable PRIVATE_KEY
echo "Attempting to capture traffic from $TARGET"
ssh -i ~/.ssh/agentkey -o StrictHostKeyChecking=no $AGENT_USER@$TARGET "tcpdump -i any -w - -U" >> /traffic/agentcapture.pcap || echo "Failed to capture traffic"

# start a netcat listener on port 1234
while true; do nc -lvnk 1234 >> /traffic/agentcapture.pcap; done || echo "Failed to start listener"