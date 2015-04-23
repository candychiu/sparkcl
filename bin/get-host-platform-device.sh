#!/usr/bin/env bash

export SPARKCL_HOME="$(cd "`dirname "$0"`"/..; pwd)"
conf_dir="${SPARKCL_HOME}/conf"
bin_dir="${SPARKCL_HOME}/bin"
lib_dir="${SPARKCL_HOME}/lib"

#RUNNING CONFIG FILE
. "${conf_dir}/sparkcl-env.sh"

echo "${SPARKCL_PLATFORM} ${SPARKCL_DEVICE}"
