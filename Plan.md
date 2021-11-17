# Project Plan
- Service defines permanent ip address for pod with DNS name
- Deployment is a blueprint for a pod
--- 
## Redis
- [ ] Make Dockerfile
- [ ] Make Kubernetes service file
    - Open service on port(and targetPort) ```6379```
    - Set DNS name to ```redis```
- [ ] Make Kubernetes deployment file
    - match label ```redis```
    - 1 replica
--- 
## RabbitMQ
- [ ] Make Dockerfile
- [ ] Make Kubernetes service file
    - Open service on port(and targetPort) ```5672```
    - Set DNS name to ```rabbitmq```
- [ ] Make Kubernetes deployment file
    - match lablel ```rabbitmq```
    - 1 replica
    - Set ```containerPort``` to ```5672```
--- 
## Playlist Generator
- [ ] Write Python script that will accept REST API requests from RabbitMQ queue, update user's model, and generate playlist based on updated model
- [ ] Make Dockerfile
- [ ] Make Kubernetes deployment file
    - match lablel ```classifier```
    - Make number of replicas scale based on cpu usage (make cpu usage average out across all pods)
    - Set ```RABBITMQ_HOST``` environment variable
    - Set ```REDDIS_HOST``` environment variable
--- 
## User Management
- [ ] Write Python script to register users, and sign in users
- [ ] Make Dockerfile
- [ ] Make Kubernetes deployment file
    - match lablel ```usermanagement```
    - Set ```RABBITMQ_HOST``` environment variable
    - Set ```REDDIS_HOST``` environment variable
--- 
## Rest
- [ ] Write python script with correct endpoints
  - [ ] Register user
    - Accept username, password (hashed)
    - Send to exchange with ```usermanagement``` tag
  - [ ] Login in user
    - Accept username, password (hashed)
    - Send to exchange with ```usermanagement``` tag
  - [ ] Request playlist generation
  - [ ] Send to exchange with ```classification``` tag
- [ ] Make Dockerfile
- [ ] Make Kubernetes service file
    - Open service on port(and targetPort) ```5000```
    - Set DNS name to ```rest```
- [ ] Make Kubernetes deployment file
    - match lablel ```rest```
    - 1 replica
    -  Set ```containerPort``` to ```5000```
--- 
## Classification Model
Test, and train model locally. Then save base model in Firestore for use as base model
- [ ] Analyse data to determine which model will work best
- [ ] Train model
- [ ] Marshall model
- [ ] Save model in Firestore

## Ingress
- [ ] Write Kubernetes ingress