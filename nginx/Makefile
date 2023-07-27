.PHONY: build push

IMAGE_NAME = nginx-service-product1
IMAGE_VERSION = latest

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) .

push:
	docker push $(IMAGE_NAME):$(IMAGE_VERSION)
