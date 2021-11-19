.PHONY: run

CONTAINER_NAME ?= 'nginx-example'
# specify path to your static folder:
STATIC_ROOT ?= /tmp
# STATIC_ROOT ?= /Users/stalk/develop/ergeon/srv-ergeon/static

run:
	docker run --rm -p 8080:80 \
	-v $(PWD)/base_nginx.conf:/etc/nginx/nginx.conf:ro \
	-v $(PWD)/nginx.conf:/etc/nginx/conf.d/default.conf:ro \
	-v $(PWD)/favicon.ico:/tmp/favicon.ico \
	-v $(STATIC_ROOT):/tmp/static \
	--name $(CONTAINER_NAME) nginx 


shell:
	docker run --rm -it --name $(CONTAINER_NAME) nginx bash
