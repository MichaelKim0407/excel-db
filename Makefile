build:
	docker-compose build --pull

lint:
	docker-compose run --rm py3.11 flake8

test3.11:
	docker-compose run --rm py3.11 pytest --cov

#test3.10:
#	docker-compose run --rm py3.10 pytest
#
#test3.9:
#	docker-compose run --rm py3.9 pytest
#
#test3.8:
#	docker-compose run --rm py3.8 pytest
#
#test3.7:
#	docker-compose run --rm py3.7 pytest

test: test3.11

ci: build lint test
