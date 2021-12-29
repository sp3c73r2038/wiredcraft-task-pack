## Environment

- terraform v1.1.2
- terraform alicloud provider plugin hashicorp/alicloud v1.149.0 (automatically installed with `terraform init`)

## Basic Info

This task is carried out with Alicloud. It will setup a VPC and two servers (one for api-server, one for db-server) in cn-shanghai region with other nessesary stuff

- ssh public key for remote ssh access
- security group and rules

To generate a real ssh key pair.

```bash
$ ssh-keygen -t ed25519 -C -f id_ed25519

# use public key in production.tf ``ssh_public_key = "..."''
$ cat id_ed25519.pub
```

file content

## Quick Start

```
# initialize provider plugin
$ terraform init

# plan phase & check output
$ make plan

# apply phase
$ make apply
```
