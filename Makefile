DOCKER_IMAGE = journal

build:
	docker build -t $(DOCKER_IMAGE) .

run:
	docker run -p 8080:8000 -v $(shell pwd)/data:/app/data $(DOCKER_IMAGE)
