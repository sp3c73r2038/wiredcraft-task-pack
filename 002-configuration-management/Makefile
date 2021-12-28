PASSWD_FILE := vault-password.txt
INVENTORY := hosts.yml
VENV := .venv
VENV_PY := $(VENV)/bin/python
PYPI := https://mirrors.163.com/pypi/simple
ANSIBLE_PLAYBOOK := .venv/bin/ansible-playbook

-include local.mk

default: setup

.venv:
	@echo ">> setup venv"
	python -m venv $(VENV)
	$(VENV_PY) -m pip install -i $(PYPI) pipenv

setup: .venv
	@echo ">> install packages"
	PIPENV_VENV_IN_PROJECT=1 $(VENV_PY) -m pipenv install -v

init:
	$(ANSIBLE_PLAYBOOK) --vault-password-file $(PASSWD_FILE) \
		-i hosts.yml playbook/init-server.yml

deploy:
	$(ANSIBLE_PLAYBOOK) --vault-password-file $(PASSWD_FILE) \
		-i hosts.yml playbook/service-deploy.yml

backup:
	$(ANSIBLE_PLAYBOOK) --vault-password-file $(PASSWD_FILE) \
		-i hosts.yml playbook/backup-database.yml
