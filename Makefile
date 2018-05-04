.DEFAULT_GOAL := run
.PHONY: clean, reset, setup


clean: # Clean build files and log files
	rm -rf **/*.pyc
	rm -rf **/__pycache__/

reset: # Delete virtual environment, database and other temporary files
	rm -rf venv

depends: # Install Python dependancies
	venv/bin/pip3 install -r requirements.txt

setup: # Setup application environment
	python3 -m venv venv
	venv/bin/pip3 install -r requirements.txt
