FORTUNE := fortune
HUGO := hugo
BIND := 127.0.0.1
PORT := 1313
NEW_POST_NAME := content/post/$(shell date +"%Y_%m_%d_%H_%M_%S")-random-post.md

define myvar
---\ndate: "$(shell date +%F)"\ntitle: "new post title $(shell date +%F)"\n---\n
endef

-include local.mk

# default action, build site and preview
default: preview

# generate random new post with fortune command
new:
	echo -e "$(myvar)" > $(NEW_POST_NAME)
	$(FORTUNE) >> $(NEW_POST_NAME)

# build site
build:
	$(HUGO)

# preview site content
preview: build
	$(HUGO) server --bind $(BIND) -p $(PORT)

# add & commit any posts, then push to upstream git repo
push:
	git add content/post
	git commit -m 'new post'
	git push origin master
