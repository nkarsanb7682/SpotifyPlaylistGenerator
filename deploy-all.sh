#!/bin/sh
kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
kubectl apply -f rabbitmq/rabbitmq-service.yaml

kubectl apply -f rest/rest-deployment.yaml
kubectl apply -f rest/rest-service.yaml
kubectl apply -f rest/rest-load-balancer.yaml

kubectl apply -f firebasesave/firebasesave-deployment.yaml