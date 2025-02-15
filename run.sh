#!/bin/sh

CPATH=$(realpath $(dirname "$0"))

. "${CPATH}/config"

#EXTRAARGS="$EXTRAARGS --log-level=debug"

env_read() {
  if [[ -f "${CPATH}/env" ]]; then
  echo "Reading env file"
    while read -r line; do
      if [[ $line =~ ^([a-zA-Z_][a-zA-Z0-9_]*)=(.*) ]]; then
        var_name="${BASH_REMATCH[1]}"
        var_value="${BASH_REMATCH[2]}"
        # escape any spaces in the value
        var_value="${var_value// /\\ }"
        echo "Setting ${var_name}"
        #export ${var_name}="${var_value}"
        ENVARS="${ENVARS} -e ${var_name}=${var_value}"
      fi
    done < "${CPATH}/env"
  fi
}

env_read

if [[ "$1" == "attach" ]]; then
  #podman exec -it ${NAME} ${ENVARS} /bin/bash
  podman exec -it ${NAME} /bin/bash
else
  podman run --hostname "${HOSTNAME}" --name "${NAME}" ${ENVARS} ${X11ARGS} ${NETARGS} ${FUSEARGS} ${SHAREDARGS} ${EXTRAARGS} ${RUNARGS} "${TAGNAME}" "$@"
  if [[ "$1" != "" ]]; then
    sleep 1
    podman attach "${NAME}"
    ./stop.sh
  fi
fi

