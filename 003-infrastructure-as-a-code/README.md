## Environment

- terraform v1.1.2

## Basic Info

This task is carried out with Alicloud. It will setup a VPC and two servers (one for api-server, one for db-server) in cn-shanghai region with other nessesary stuff

- ssh public key for remote ssh access
- security group and rules

To generate a real ssh key pair.

```bash
$ ssh-keygen -t ed25519 -C -f id_ed25519

# use public key in ssh.tf
$ cat id_ed25519.pub
```

file content

```
.
├── README.md
├── security.tf    # Security group & rules
├── server.tf      # ECS server definition
├── ssh.tf         # SSH key
├── vars.tf        # API key
└── vpc.tf         # Network
```

## Quick Start
