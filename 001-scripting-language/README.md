## Basic Environment & Info

OS: Gentoo Linux (any mordern GNU/Linux system will do)
Python: 3.9

Also assume these tools and commands are installed and available.

- `make`
- `hugo`
- `fortune`

Hugo theme named [Even](https://themes.gohugo.io/themes/hugo-theme-even/) is embedded with a git sub repo.

## Quick Start

For most situation, I prefer using `make`. To demostrating my ability to write script, a Python version is also provided.

### Makefile version

```bash
# to build & preview
$ make

# generate random new post content
$ make new

# build site
$ make build

# preview
$ make preview

# git push
$ make push
```

Now open http://localhost:1313/.

To customize variables in Makefile. Using `local.mk` to override.

```Make
# local.mk
BIND := 0.0.0.0
PORT := 4000
```

### Python script version

```bash
# generate random new post content
$ python manage.py new

# build site
$ python manage.py build

# preview
$ python manage.py preview

# git push
$ python manage.py push

# see options
$ python manage.py --help
$ python manage.py {cmd} --help
```
