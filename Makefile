.PHONY: clean deps-py run

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean       => to clean clean all automatically generated files"
	@echo "  deps-py     => to update Python packages"
	@echo "  run         => to run development server"

clean:
	find src/ -name \*.pyc -delete
	find src/ -name \*__pycache__ -delete

deps-py:
	pip install -U -r requirements.txt

run: clean
	cd src/ && python poffw.py
