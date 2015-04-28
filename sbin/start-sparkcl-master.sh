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

python -c "open('${SPARK_HOME}/conf/spark-env.sh','w').write('#!/usr/bin/env bash\nexport SPARK_MASTER_IP=${1}\n')"
python -c "import time;open('${SPARKCL_HOME}/work/log/master/logs.txt','w').write('%s - SparkCL Master Started\n'%(time.strftime('%H:%M:%S')))"
if [ -z ${SPARK_MASTER_IP:+x} ];
    then
        echo -e "\nSPARK_MASTER_IP is unset.\nPlease set SPARK_MASTER_IP in SPARK_HOME/conf/spark-env.sh\n";
        exit
fi

if [ -z ${SPARKCL_WEBUI_PORT:+x} ];
    then export SPARKCL_WEBUI_PORT=8081
fi

#START SPARK MASTER
echo -n "Starting Spark Master         "
cd "${SPARK_HOME}/sbin"; "./start-master.sh" > /dev/null 2>&1

counter=1
spark_master_check=$(netstat -an | grep ${SPARK_MASTER_IP}:7077)
while [ $counter -le 10 ]
do
    counter=$(( $counter + 1 ))
    if [ -z ${spark_master_check:+x} ];
    then
        spark_master_check=$(netstat -an | grep ${SPARK_MASTER_IP}:7077)
    else
        echo -e "[${green}OK${NC}]"
        break
    fi

    if [ $counter -eq 11 ];
        then
        echo -e "[${red}FAILED${NC}]"
        echo "Please check SPARK_MASTER_IP in SPARK_HOME/conf/spark-env.sh"
        exit
    fi
    sleep 1

done
#START SPARKCL CGI SERVER

echo -n "Starting SparkCL Master        "

cd "${lib_dir}/network/cgi-bin/"; nohup python "master_cgiserver.py" "${SPARK_MASTER_IP}" "${SPARKCL_WEBUI_PORT}"  > /dev/null 2>&1 &

counter=1
sparkcl_cgi_checker=$(netstat -an | grep ${SPARK_MASTER_IP}:${SPARKCL_WEBUI_PORT})
while [ $counter -le 5 ]
do
    counter=$(( $counter + 1 ))
    if [ -z ${sparkcl_cgi_checker:+x} ];
    then
        sparkcl_cgi_checker=$(netstat -an | grep ${SPARK_MASTER_IP}:${SPARKCL_WEBUI_PORT})
    else
        echo -e "[${green}OK${NC}]"
        break
    fi

    if [ $counter -eq 6 ];
    then
        echo -e "[${red}FAILED${NC}]"
        exit
    fi
    sleep 1
done


echo -e "\n${green}SparkCL master started.${NC}";
echo -e "SPARKCL_WEBUI = http://${SPARK_MASTER_IP}:${SPARKCL_WEBUI_PORT}"
echo -e "SPARK_MASTER_IP    = spark://${SPARK_MASTER_IP}:7077 "
cd "${SPARKCL_HOME}/sbin/"; python sparkcl-master.py "${SPARK_MASTER_IP}" > /dev/null 2>&1 &
