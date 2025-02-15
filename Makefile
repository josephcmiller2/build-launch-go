include config.mak

all:
	TMPDIR=$(TMPDIR) time podman build --tag $(TAGNAME) -f ./Dockerfile

distclean:
	rm -f config.mak

remove: rm

rm:
	podman rm $(NAME)

list: ls

ls:
	podman ps -a

.PHONY: all remove rm list ls
