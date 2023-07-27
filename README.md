# api-gateways
# Comparison of API-GW (KrakenD vs. Kong)

KrakenD and Kong are both popular open-source API gateways, but they have some differences in functionality and architecture. Here are some differences, advantages, and disadvantages of both solutions:

## KrakenD:

KrakenD is a lightweight API gateway designed for high performance and low latency. It uses declarative configuration in JSON or YAML.
### Advantages:
High Performance: KrakenD is specialized in serving APIs quickly and efficiently.
Easy Configuration: KrakenD's declarative configuration allows for easy and fast customization of the gateway.
Low Resource Consumption: KrakenD is resource-friendly and can be deployed on less powerful hardware environments.
### Disadvantages:
Limited Feature Set: Compared to Kong, KrakenD may offer fewer built-in features and extension possibilities.

## Kong:

Kong is a feature-rich API gateway that provides a wide range of functionalities such as load balancing, authentication, logging, and plugin systems for advanced customization.
### Advantages:
Extensive Features: Kong offers many built-in features and plugins that can be used in various use cases.
Scalability: Kong is highly scalable and can be deployed in high-performance environments.
Plugin Extensions: Kong's plugin system allows for adding additional functionalities and extensions.
### Disadvantages:
Complex Configuration: Kong's configuration can be more complex as it is based on a multi-layered architecture.
Higher Resource Consumption: Due to its extensive functionality, Kong may require more resources compared to KrakenD.

It is important to note that the choice between KrakenD and Kong depends on the specific requirements of your project. If you are looking for a lightweight, performant solution and your requirements are simple, KrakenD might be the appropriate choice. However, if you need extensive features, extensibility, and an established ecosystem, Kong may be the better option.

### Deployment
```shell
helm repo add equinixmetal https://helm.equinixmetal.com
```

# KrakenD
## Links
* https://www.krakend.io/docs/overview/guides/

## configuration
### krakend.json
```json
{
  "version": 3,
  "name": "My API GW",
  "port": 8080,
  "cache_ttl": "3600s",
  "timeout": "3s",
  "extra_config": {
    "telemetry/logging": {
      "level":  "DEBUG",
      "prefix": "[KRAKEND]",
      "syslog": false,
      "stdout": true
    },
    "telemetry/metrics": {
      "collection_time": "60s",
      "proxy_disabled": false,
      "router_disabled": false,
      "backend_disabled": false,
      "endpoint_disabled": false,
      "listen_address": ":8090"
    },
    "security/cors": {}
  },
  "endpoints": [
    {
      "endpoint": "/product1",
      "method": "GET",
      "output_encoding": "no-op",
      "extra_config": {},
      "backend": [
        {
          "url_pattern": "/product1-index.html",
          "encoding": "no-op",
          "sd": "static",
          "method": "GET",
          "extra_config": {},
          "host": [
            "http://product1.nginx.svc.cluster.local"
          ],
          "disable_host_sanitize": true
        }
      ]
    },
    {
      "endpoint": "/product2",
      "method": "GET",
      "output_encoding": "no-op",
      "extra_config": {},
      "backend": [
        {
          "url_pattern": "/product2-index.html",
          "encoding": "no-op",
          "sd": "static",
          "method": "GET",
          "extra_config": {},
          "host": [
            "http://product2.nginx.svc.cluster.local"
          ],
          "disable_host_sanitize": true
        }
      ]
    }
  ]
}
```
### create the configmap for krakend
```shell
kubectl create configmap krakend-cfg --from-file=./krakend-cfg.json -n krakend
```
---
## KrakenD playground
- youtube: https://www.youtube.com/watch?v=VtXXZRO84t8
- link: https://github.com/krakendio/playground-community
- clone repo
```shell
git clone https://github.com/krakendio/playground-community.git
```
```shell
docker-compose up
```
using devopsfaith/krakend:watch
- watch tag is for development only and will restart Krakend every time when there is a configuration change.





---
# LDAP
## deploying the files
creating namespace
```shell
kubectl create ns ldap
```
applying the files
```shell
kubectl apply -f openldap-pvc.yaml
kubectl apply -f openldap-nginx-deployment.yaml
kubectl apply -f openldap-service.yaml
```
creating user
```shell
kubectl -n ldap exec -it [POD_NAME] -- /bin/bash
```
creating the ou-user.ldif
```shell
echo -e "dn: ou=users,dc=proconion,dc=com\nobjectClass: organizationalUnit\nou: users" > ou-user.ldif
```
adding the ou-user.ldif
```shell
ldapadd -x -D "cn=admin,dc=proconion,dc=com" -w adminpassword -f ou-user.ldif
```

Inside the container, create a file named user.ldif
```shell
echo -e "dn: uid=username,ou=users,dc=proconion,dc=com\nobjectClass: top\nobjectClass: account\nobjectClass: simpleSecurityObject\nuserPassword: mypassword\nuid: username" > user.ldif
```
```shell
dn: uid=username,ou=users,dc=proconion,dc=com
objectClass: top
objectClass: account
objectClass: simpleSecurityObject
userPassword: mypassword
uid: username
```
add the user:
```shell
ldapadd -x -D "cn=admin,dc=proconion,dc=com" -w adminpassword -f user.ldif
```
verify if user is created
```shell
kubectl -n ldap exec [POD_NAME] -- ldapsearch -x -LLL -H ldap://localhost:389 -D "cn=admin,dc=proconion,dc=com" -w adminpassword -b "ou=users,dc=proconion,dc=com" "(uid=username)"
```
---
# Kong
## installation with Manifest
```shell
kubectl apply -f https://raw.githubusercontent.com/Kong/kubernetes-ingress-controller/v2.10.0/deploy/single/all-in-one-dbless.yaml
```
## installation with helm
- https://docs.konghq.com/gateway/3.3.x/install/kubernetes/helm-quickstart/
```shell
helm upgrade --install kong-poc ./kong -f ./kong/values.yaml -n kong
```