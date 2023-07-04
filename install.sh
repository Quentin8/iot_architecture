#!/bin/bash
set -e

git clone https://github.com/Quentin8/iot_architecture.git

cd iot_architecture

echo "Installing helm"
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm

echo installing VerneMQ MQTT broker
helm repo add vernemq https://vernemq.github.io/docker-vernemq
helm install vernemq -f vernemq_values.yaml vernemq/vernemq

echo installing filebeat agent
helm repo add elastic https://helm.elastic.co
helm install filebeat -f filebeat_values.yaml elastic/filebeat

echo installing logstash:
helm repo add elastic https://helm.elastic.co
helm install -f logstash_values.yaml logstash elastic/logstash


echo installing influxdb :
helm repo add influxdata https://helm.influxdata.com/
helm install -f influxdb_values.yaml influxdb influxdata/influxdb2
