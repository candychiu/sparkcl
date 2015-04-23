#!/usr/bin/env bash


spark_master_check=$(netstat -an | grep ${SPARK_MASTER_IP}:7077)
sparkcl_cgi_checker=$(netstat -an | grep ${SPARK_MASTER_IP}:${SPARKCL_WEBUI_PORT})


if [ -z ${spark_master_check:+x} ];
    then
    echo -e "Spark master is not running.";
else
    echo -e "Spark master is running."
fi



if [ -z ${spark_master_check:+x} ];
    then
    echo -e "SparkCL master is not running.";
else
    echo -e "SparkCL master is running."
fi
