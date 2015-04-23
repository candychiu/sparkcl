#!/usr/bin/env bash

export SPARKCL_HOME="$(cd "`dirname "$0"`"/..; pwd)"
export SPARK_HOME="$(cd "`dirname "$0"`"/../..; pwd)"


conf_dir="${SPARKCL_HOME}/conf"
bin_dir="${SPARKCL_HOME}/bin"
lib_dir="${SPARKCL_HOME}/lib"
work_dir="${SPARKCL_HOME}/work"

#RUNNING CONFIG FILE
. "${conf_dir}/sparkcl-env.sh"
. "${SPARK_HOME}/conf/spark-env.sh"



#GENERATE PYTHON CODE
python "${lib_dir}/generate-spark-code.py" "${SPARKCL_PLATFORM}" "${SPARKCL_DEVICE}" "1" "${SPARKCL_HOME}" "$(date +"code_%m%d%Y%S.py")"
