DOCKER_IMAGE = journal

dev:
	uv run uvicorn journal:app --host 0.0.0.0 --port 8000 --reload --log-config log_conf.yaml

build:
	docker build -t $(DOCKER_IMAGE) .

run:
	docker run -p 8080:8000 -v $(shell pwd)/data:/app/data $(DOCKER_IMAGE)
