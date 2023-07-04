# IoT Kubernetes Architecture

The following  project is an IoT architecture suggestion based on Kubernetes.

![Architectural Schema](./resources/img/schema.png)

Features:
- easily deployed in cloud or edge environments
- scalable
- fast sensors to cloud deployment
- supports multiple input protocols (see : https://www.elastic.co/guide/en/logstash/current/input-plugins.html)

## Configuration
Don't forget to change user, password and token inside *influxdb_values.yaml* file:

```yml
adminUser:
  user: "admin"
  password: "Jfehhnenkzfg"
  token: "jbbeZEVESnzuNEBCeivnenkoOJIBZFEJl_555NKINBCZ_nbn54BnNCBNDZK?D?IKNZ=="
```

Then replace the following parameters inside logstash_values.yaml file :
- CHANGEME_WITH_INFLUXDB_TOKEN
- MY_INFLUXDB_HOST

```conf
      http {
        url => "http://MY_INFLUXDB_HOST/api/v2/write?org=influxdata&bucket=sensors&precision=ns"
        http_method => "post"
        headers => {
          "Authorization" => "Token CHANGEME_WITH_INFLUXDB_TOKEN" 
          "Content-Type" => "text/plain; charset=utf-8"
          "Accept" => "application/json"
        }
        format => "message"
        # Peut etre ajouter un tag de localisation
        message => "sensors,site=%{siteid},sensor=%{mysensor} %{mymetric}=%{value} %{unix_timestamp}000000000"
      }
```

## Installation

### Kubernetes (k3s)
Connect onto your server, then :

```
curl -sfL https://get.k3s.io | sh -
```

### Stack
Here are the values.yaml files definitions:

- filebeat: https://github.com/elastic/helm-charts/tree/main/filebeat
- influxdb2: https://github.com/influxdata/helm-charts/blob/master/charts/influxdb2/values.yaml
- logstash: https://github.com/elastic/helm-charts/tree/main/logstash
- verneMQ: https://github.com/vernemq/docker-vernemq/tree/master/helm/vernemq#configuration

```
bash install.sh
```

## Try it

Download mosquitto client and execute : 

```
mosquitto_pub -h "10.30.50.201" -t "sensors/maison2/chambre1/humidity" -m "45" -p 31111
```
- maison2: is the site
- chambre1: the sensor name
- humidity: the measurement

To see the data, connect to MY_INFLUXDB_HOST with adminUser.user and adminUser.password from influxdb_values.yaml

Click on Data Explorer, select sensors in FROM, then sensors in _measurement, then the metric type (humidity, temperature,...). Then you can fileter with site or sensor value.
