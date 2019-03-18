#!/usr/bin/env bash

cd test_db

export DB_HOST=${DB_HOST:=0.0.0.0}
export DB_USER=${DB_USER:=root}
export DB_PASSWORD=${DB_PASSWORD:=mysql-pass}
export DB_NAME=${DB_NAME:=employees}
export DB_PORT=${DB_PORT:=3306}

export DEST_DB_HOST=${DEST_DB_HOST:=0.0.0.0}
export DEST_DB_USER=${DEST_DB_USER:=root}
export DEST_DB_PASSWORD=${DEST_DB_PASSWORD:=mysql-pass}
export DEST_DB_NAME=${DEST_DB_NAME:=employees_2}
export DEST_DB_PORT=${DEST_DB_PORT:=9999}

docker stop dest_mysql
docker rm dest_mysql
docker stop src_mysql
docker rm src_mysql

docker pull mysql:5.7.25
docker build -t mysql_task ../
docker run -p ${DB_PORT}:3306 --name src_mysql -e MYSQL_ROOT_PASSWORD=${DB_PASSWORD} -d mysql_task
docker run -p ${DEST_DB_PORT}:3306 --name dest_mysql -e MYSQL_ROOT_PASSWORD=${DB_PASSWORD} -d mysql_task

echo "Wait for running db"
for i in {0..30}; do echo -n "*"; sleep 1; done
echo -e "\n"

mysql --user=${DB_USER} --password=${DB_PASSWORD} -h ${DB_HOST} < employees.sql
mysql --user=${DEST_DB_USER} --password=${DEST_DB_PASSWORD} -h ${DB_HOST} --port=${DEST_DB_PORT} < employees_wo_titles.sql

cd -
