VERSION=v4
DOCKERUSER=387527458246

build:
	docker build -f Dockerfile -t angular-fe .

push:
	docker tag angular-fe $(DOCKERUSER)/angular-fe:$(VERSION)
	docker push $(DOCKERUSER)/angular-fe:$(VERSION)
	docker tag angular-fe $(DOCKERUSER)/angular-fe:latest
	docker push $(DOCKERUSER)/angular-fe:latest
