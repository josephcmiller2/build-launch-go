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
  apt-get install -y nodejs npm

RUN \
  npm install -g tailwindcss

ENV TZ=America/Denver
ENV DEBIAN_FRONTEND=noninteractive

ENV HOME=/root

# Define working directory.
WORKDIR /buildlaunchgo

EXPOSE 1080 1081

# Start systemd
ENTRYPOINT ["/usr/sbin/init"]

# Define default command.
CMD ["bash"]
