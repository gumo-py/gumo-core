package_name = gumo-core

.PHONY: setup
setup:
	pip install twine wheel pytest
	pip install -r requirements.txt

.PHONY: deploy
deploy: clean build
	python -m twine upload \
		--repository-url https://upload.pypi.org/legacy/ \
		dist/*

.PHONY: test-deploy
test-deploy: clean build
	python -m twine upload \
		--repository-url https://test.pypi.org/legacy/ \
		dist/*

.PHONY: test-install
test-install:
	pip --no-cache-dir install --upgrade \
		-i https://test.pypi.org/simple/ \
		${package_name}

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf ${package_name}.egg-info dist build

.PHONY: pip-compile
pip-compile:
	pip-compile --output-file requirements.txt requirements.in

.PHONY: test
test:
	PYTHONPATH=. pytest -v tests
