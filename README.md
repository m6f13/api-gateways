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

### create the configmap for nginx
```shell
kubectl create configmap product1-html --from-file=product1-index.html -n nginx
kubectl create configmap product2-html --from-file=product2-index.html -n nginx
```

### deploy ingress controller
```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
```