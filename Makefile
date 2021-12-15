PYPROJECT = pyproject.toml
DOCKERFILE = Dockerfile

list:
	@sh -c "$(MAKE) -p no_targets__ | \
		awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {\
			split(\$$1,A,/ /);for(i in A)print A[i]\
		}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"

# required for list
no_targets__:

clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

format: clean
	@poetry run black --config $(PYPROJECT) shelf/ tests/
	@poetry run isort --settings-path $(PYPROJECT) shelf/ tests/

test:
	@poetry run coverage run --rcfile $(PYPROJECT) -m pytest tests/ "$*"
	@poetry run coverage html --rcfile $(PYPROJECT)

build_dev:
	docker build --rm --tag shelf:test --file $(DOCKERFILE) --target test .

build_prod:
	docker build --rm --tag shelf --file $(DOCKERFILE) . 

run_dev:
	docker run -it shelf:test bash

run_prod:
	docker run -it shelf:latest bash

docker_lsc:
	docker ps --last=10 --format="table {{.ID}}\\t{{.Image}}\\t{{.Status}}\\t{{.Names}}"

docker_lsi:
	docker images

rmi:
	docker rmi -f shelf
	docker rmi -f shelf:test
	
prune:
	docker image prune -f
	docker container prune -f