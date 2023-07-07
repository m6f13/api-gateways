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

# Deployment
## KrakenD
create a namespace: krakend

Create a file named krakend-deployment.yaml and add the following content:
````yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: krakend
  namespace: krakend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: krakend
  template:
    metadata:
      labels:
        app: krakend
    spec:
      containers:
        - name: krakend
          image: devopsfaith/krakend:latest
          ports:
            - containerPort: 8080  # Port for accessing the KrakenD API Gateway
          volumeMounts:
            - name: config-volume
              mountPath: /etc/krakend
      volumes:
        - name: config-volume
          configMap:
            name: krakend-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: krakend-config
  namespace: krakend
data:
  krakend-config.yaml: |
    version: 2
    timeout: 3000ms
    endpoints:
    - endpoint: /service1
      method: GET
      extra_config:
        github_com/devopsfaith/krakend-gologging/logging:
          level: DEBUG
      backend:
      - url_pattern: /filename1.txt
        host: nginx.nginx.svc.cluster.local
        encoding: json
````

Run the following command to create the deployment:
````shell
kubectl apply -f krakend-deployment.yaml
````
## NGINX
create a namespace: nginx

Create a file named nginx-deployment.yaml and add the following content:
````yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80  # Port for accessing NGINX
          volumeMounts:
            - name: nginx-volume
              mountPath: /usr/share/nginx/html
      volumes:
        - name: nginx-volume
          emptyDir: {}

````
Run the following command to create the NGINX service:
````shell
kubectl apply -f nginx-deployment.yaml
````
Execute the following command to start a temporary pod instance and create the filename1.txt file:
````shell
kubectl run temp-pod --restart=Never --image=nginx --namespace=nginx --dry-run=client -o yaml -- /bin/sh -c "echo 'Hello, World!' > /usr/share/nginx/html/filename1.txt"
````
This command creates a temporary pod instance using the NGINX image and writes the content "Hello, World!" to the filename1.txt file in the /usr/share/nginx/html/ directory.

Test the Use Case:
To test the use case, run the following command:
````shell
wget http://krakend.krakend:8080/service1/filename1.txt
````
This command sends the request through the KrakenD API Gateway (krakend.krakend:8080) and performs the request mapping from /service1 to the /filename1.txt path in the NGINX service. The filename1.txt file is downloaded.
