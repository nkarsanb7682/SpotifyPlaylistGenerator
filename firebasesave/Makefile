VERSION=v4
DOCKERUSER=387527458246

build:
	docker build -f Dockerfile-firebasesave -t firebasesave .

push:
	docker tag firebasesave $(DOCKERUSER)/firebasesave:$(VERSION)
	docker push $(DOCKERUSER)/firebasesave:$(VERSION)
	docker tag firebasesave $(DOCKERUSER)/firebasesave:latest
	docker push $(DOCKERUSER)/firebasesave:latest
