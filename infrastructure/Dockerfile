#
# PHP Dockerfile
#
# https://hub.docker.com/_/php
#

# Pull base image.
FROM ubuntu:24.04

RUN \
  apt-get update && \
  apt-get install -y gnupg wget software-properties-common vim

RUN \
  apt-get install -y python3-pip aptitude

RUN \
  apt-get install -y python3-flask python3-sqlalchemy python3-flask-cors

ENV TZ=America/Denver
ENV DEBIAN_FRONTEND=noninteractive

ENV HOME=/root

# Define working directory.
WORKDIR /backend

EXPOSE 1082

# Start systemd
ENTRYPOINT ["/usr/sbin/init"]

# Define default command.
CMD ["bash"]
