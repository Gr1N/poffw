.PHONY: clean deps-py deps-js run

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean       => to clean clean all automatically generated files"
	@echo "  deps-py     => to update Python packages"
	@echo "  deps-js     => to update JavaScript packages"
	@echo "  run         => to run development server"

clean:
	find src/ -name \*.pyc -delete
	find src/ -name \*__pycache__ -delete

deps-py:
	pip install -U -r requirements.txt

deps-js:
	npm install
	npm run build

run: clean
	cd src/ && python poffw.py
