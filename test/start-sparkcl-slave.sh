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


if [ -z $1 ] || [ -z $2 ];
then
    echo "start-sparkcl-slave [master_ip] [slave_ip]"
    exit
fi

. "${SPARK_HOME}/conf/spark-env.sh"
. "${conf_dir}/sparkcl-env.sh"

sudo python "${SPARKCL_HOME}/test/sparkcl-slave.py" "$1" "$2" "${SPARK_HOME}"
