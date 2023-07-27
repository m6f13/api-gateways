# LDAP Middleware with KrakenD

This project provides a middleware service that interacts with an OpenLDAP server for user authentication. The service is meant to be used with KrakenD to authenticate requests before forwarding them to other services, such as NGINX.

## Prerequisites

- Docker
- Kubernetes (kubectl & a running cluster)
- Make utility

## Docker Build Steps

1. Ensure your Docker daemon is running.
2. Navigate to the project directory.

### Modify requirements

1. Update `requirements.txt` with necessary Python packages.
    - `flask==2.3.2`
    - `python-ldap==3.4.3`

### Building the Docker Image

1. From the project root, run:
```shell
make build
```
This will use the Makefile to build a Docker image with the necessary dependencies and project files.

