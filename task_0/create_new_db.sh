#!/usr/bin/env bash

cd test_db

export DB_HOST=${DB_HOST:=0.0.0.0}
export DB_USER=${DB_USER:=root}
export DB_PASSWORD=${DB_PASSWORD:=mysql-pass}
export DB_NAME=${DB_NAME:=employees}

export DEST_DB_HOST=${DEST_DB_HOST:=0.0.0.0}
export DEST_DB_USER=${DEST_DB_USER:=root}
export DEST_DB_PASSWORD=${DEST_DB_PASSWORD:=mysql-pass}
export DEST_DB_NAME=${DEST_DB_NAME:=employees_2}

docker stop mysql
docker rm mysql

docker pull mysql:5.7.25
docker build -t mysql_task ../
docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=${DB_PASSWORD} -d mysql_task

echo "Wait for running db"
for i in {0..30}; do echo -n "*"; sleep 1; done
echo -e "\n"

mysql --user=${DB_USER} --password=${DB_PASSWORD} -h ${DB_HOST} < employees.sql
mysql --user=${DEST_DB_USER} --password=${DEST_DB_PASSWORD} -h ${DB_HOST} < employees_wo_titles.sql

cd -
