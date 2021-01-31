.PHONY: all prepare-dev
.SILENT: run
SHELL=/bin/bash

VENV_NAME?=.venv
VENV_BIN=$(shell pwd)/${VENV_NAME}/bin
VENV_ACTIVATE=${VENV_BIN}/activate

PYTHON=${VENV_BIN}/python3

all:
	@echo "make prepare-dev"
	@echo -e "\tCreates and install all development dependencies"
	@echo "make clean"
	@echo -e "\tClean all dependencmaes and virtual enviroment"
	@echo "make viewlog"
	@echo -e "\tDisplays pip install log"
	@echo "make dist"
	@echo -e "\tCreate a archive to be deployed."
	@echo "make install"
	@echo -e "\tInstall the package locally."
	@echo "make install-global"
	@echo -e "\tInstall the package globaly."
	@echo "make uninstall"
	@echo -e "\tUninstall the package."
	@echo "make update"
	@echo -e "\tUpdates and installs  new version"
prepare-dev: create-venv

man:

create-venv:
	@echo -e "\e[35mChecking If env Exists\e[0m"
	@if [[ ! -d ${VENV_NAME} ]]; then \
		echo -e "\e[34mCreating Virtual enviroment\e[0m"; \
		python3 -m venv ${VENV_NAME}; \
		chmod +x ${VENV_ACTIVATE}; \
		echo -e "\e[34mActivating venv\e[0m"; \
		source ${VENV_ACTIVATE}; \
		echo -e "\e[34mInstalling dependencies (check .pip.log for output)\e[0m"; \
		pip install --upgrade pip setuptools > .pip.log; \
		pip install -r requirements.txt >> .pip.log; \
		echo -e  "\e[32mUse 'source .venv/bin/activate'\e[0m"; \
	fi
clean:
	echo -e "\e[31mCleaning Enviroment\e[0m"
	@find . -name '*.pyc'       -delete
	@find . -name '__pycache__' -delete
	@rm -rf $(VENV_NAME) *.eggs *.egg-info dist build docs/_build .cache
dist:
	python3 ./setup.py sdist bdist_wheel
install: dist
	pip3 install --user dist/*.tar.gz
install-global: dist
	pip3 install dist/*.tar.gz
viewlog:
	less .pip.log
uninstall:
	pip3 uninstall infracalc
update:
	make uninstall
	git pull origin main
	make clean install
clean-dist:
	rm -rf dist/
