#!/bin/sh

CPATH=$(realpath $(dirname "$0"))

. "${CPATH}/config"


podman stop "${NAME}"
podman rm "${NAME}"

