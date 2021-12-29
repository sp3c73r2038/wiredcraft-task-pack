## Environment

I'm using GitHub Action for workflow pipeline.

See `.github/workflows/`

- `build-docker-image.yml` for build docker image.
- `unittest.yml` for running unit tests.
- `deploy.yml` for deploy application to server (for demonstration purpose).

Deploying is using ansible, playbook is in this folder.

Visit GitHub Repo action page to see results in action.

Note: the `deploy` workflow is for demonstration purpose, can not run without proper environment.

## Quick Start

All credential and password is protected by `ansible-vault`.
To use them, provide a password file (set secrets in repo settings when using GitHub Action)

```bash
# This password is actually used for demonstration purpose
$ echo 'ThisIsMyVaultS3cr37' > vault-password.txt
```

To see vault encrypted secrets

```bash
$ .venv/bin/ansible-vault view --vault-password-file vault-password.txt group_vars/api/vault
```
