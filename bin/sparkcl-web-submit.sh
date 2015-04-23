#!/usr/bin/env bash

export SPARKCL_HOME="$(cd "`dirname "$0"`"/..; pwd)"
export SPARK_HOME="$(cd "`dirname "$0"`"/../..; pwd)"
PYTHONPATH=$PYTHONPATH:$SPARKCL_HOME/lib
export PYTHONPATH

conf_dir="${SPARKCL_HOME}/conf"
bin_dir="${SPARKCL_HOME}/bin"
lib_dir="${SPARKCL_HOME}/lib"
work_dir="${SPARKCL_HOME}/work"

. "${conf_dir}/sparkcl-env.sh"
. "${SPARK_HOME}/conf/spark-env.sh"


#SUBMIT
"${SPARK_HOME}/bin/spark-submit" "--py-files" "${lib_dir}/sparkcl.py" "${1}" 
