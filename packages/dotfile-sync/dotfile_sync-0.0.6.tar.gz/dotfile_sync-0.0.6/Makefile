.ONE_SHELL:
.PHONY: build publish_to_pypi

build:
	rm -rf dist && python -m build

publish_to_pypi: build
	twine upload --repository pypi dist/*