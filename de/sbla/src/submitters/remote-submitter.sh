#!/bin/bash
set -a
source .env
set +a
if [ "$IP" == "" ]; then
  echo "check .env, no IP defined"
  exit
fi
if [ "$USER" == "" ]; then
  echo "check .env, no USER defined"
  exit
fi
if [ "USER_KEY" == "" ]; then
  echo "check .env, no USER_KEY defined"
  exit
fi
if ! [ -f $USER_KEY ]; then
  echo "check .env: $USER_KEY does not exist"
  exit
fi
scp -r -oStrictHostKeyChecking=no -i $USER_KEY ../scripts $USER@$IP:/home/$USER/ 2>&1 >/dev/null
scp -r -oStrictHostKeyChecking=no -i $USER_KEY ../../data.json $USER@$IP:/home/$USER/ 2>&1 >/dev/null
ssh -oStrictHostKeyChecking=no -i $USER_KEY $USER@$IP "ls /home/$USER/scripts | while read line; do docker cp /home/$USER/scripts/\$line \$(docker ps -l -q):/data/; done" 2>&1 >/dev/null
ssh -oStrictHostKeyChecking=no -i $USER_KEY $USER@$IP "ls /home/$USER/ | grep json | while read line; do docker cp /home/$USER/\$line \$(docker ps -l -q):/data/; done" 2>&1 >/dev/null
ssh -oStrictHostKeyChecking=no -i $USER_KEY $USER@$IP "docker exec \$(docker ps -l -q) chmod -R a+rwx /data/" 2>&1 >/dev/null
if ! [ "$1" == "upload" ]; then
  ssh -oStrictHostKeyChecking=no -i $USER_KEY $USER@$IP "docker exec -u egrep \$(docker ps -l -q) /bin/bash -c '
      cd /lessons/dags && \
      HADOOP_CONF_DIR=/etc/hadoop/conf \
      SPARK_HOME=/usr/lib/spark \
      PYTHONPATH=/usr/local/lib/python3.8 \
      PYSPARK_PYTHON=/usr/bin/python3 \
      spark-submit \
       /data/$1 "${@:2}" \
  '"
fi