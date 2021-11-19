.PHONE: run

CONTAINER_NAME ?= 'gunicorn-example'

build:
	docker build -t $(CONTAINER_NAME) .

run: build
	docker run --rm -p 9999:9999 \
	-v $(PWD)/../src/app.py:/usr/src/app/app.py \
	--name $(CONTAINER_NAME) $(CONTAINER_NAME) \
	gunicorn -b 0.0.0.0:9999 -w 2 app:web_app

shell: build
	docker run --rm -it --name $(CONTAINER_NAME) $(CONTAINER_NAME) bash

python: build
	docker run --rm -it --name $(CONTAINER_NAME) $(CONTAINER_NAME)
