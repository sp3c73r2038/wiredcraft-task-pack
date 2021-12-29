## Environment

- OS: Gentoo Linux
- Ansible

All python package is installed using virtualenv and [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html).

Remember to export environment variable `PIPENV_VENV_IN_PROJECT` to setup the virtualenv in this folder.

```bash
$ export PIPENV_VENV_IN_PROJECT=1
```

If pipenv is not installed, you can initialize the virtualenv manually

```bash
$ python -m venv .venv
```

then install pipenv

```bash
$ .venv/bin/pip install pipenv

# for faster network access in China
$ .venv/bin/pip install -i https://mirrors.163.com/pypi/simple pipenv
```

then setup packages

```bash
$ .venv/bin/pipenv install
```

to run any command from virtualenv

```bash
$ .venv/bin/pipenv run ansible

# or rather use ``pyx'' script I wrote from top bin folder
$ /path/to/pyx ansible
```

## Basic Info

Assume we are using a server running Debian system with MySQL as database.

Remote server with Debian system should meet this requirements

- remote SSH non-root user has been setup and has permission to sudo
- remote SSH non-root user is in `docker` group to interactive with docker service
- system has python interpreter to run ansible task

We need to at least these software.

- docker for running API application
- database
- nginx for web serving

To abstract server inventory, use this ssh config for convenient purpose

```conf
# put this line in your ~/.ssh/config, after test just comment it out or delete this line
Include ~/.ssh/config_local

# put this line in your ~/.ssh/config_local
Host api-server
  Hostname <what ever the actual server ip or hostname>
  User <actual user>
  Port <actual port>

Host db-server
  Hostname <what ever the actual server ip or hostname>
  User <actual user>
  Port <actual port>
```

## Quick Start

All credential and password is protected by `ansible-vault`.
To use them, provide a password file

```bash
# This password is actually used for demostrating purpose
$ echo 'ThisIsMyVaultS3cr37' > vault-password.txt
```

to run any playbook

```bash
# playbook/init-server.yml
# playbook/service-deploy.yml
# playbook/database-backup.yml
$ .venv/bin/pipenv run ansible-playbook --vault-password-file vault-password.txt -i hosts.yml playbook/<playbook_to_run>.yml
```

or use `make`

```bash
$ make setup
$ make init
$ make deploy
$ make backup
```

To override any variable in `Makefile`, use `local.mk`.
