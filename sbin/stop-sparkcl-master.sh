#!/usr/bin/env bash

export SPARKCL_HOME="$(cd "`dirname "$0"`"/..; pwd)"
export SPARK_HOME="$(cd "`dirname "$0"`"/../..; pwd)"
conf_dir="${SPARKCL_HOME}/conf"
bin_dir="${SPARKCL_HOME}/bin"
lib_dir="${SPARKCL_HOME}/lib"
work_dir="${SPARKCL_HOME}/work"


. "${SPARK_HOME}/conf/spark-env.sh"
. "${conf_dir}/sparkcl-env.sh"

cd "${SPARK_HOME}/sbin"; "./stop-master.sh" > /dev/null 2>&1
kill $( lsof -t -i:9090)
