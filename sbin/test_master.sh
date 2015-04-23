#!/usr/bin/env bash

export SPARKCL_HOME="$(cd "`dirname "$0"`"/..; pwd)"
export SPARK_HOME="$(cd "`dirname "$0"`"/../..; pwd)"
conf_dir="${SPARKCL_HOME}/conf"
bin_dir="${SPARKCL_HOME}/bin"
lib_dir="${SPARKCL_HOME}/lib"
work_dir="${SPARKCL_HOME}/work"

echo;

green='\033[1;32m'
NC='\033[0m' # No Color
red='\033[1;31m'


. "${SPARK_HOME}/conf/spark-env.sh"
. "${conf_dir}/sparkcl-env.sh"

cd "${SPARKCL_HOME}/sbin/"; python sparkcl-master.py "${SPARK_MASTER_IP}"
