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

