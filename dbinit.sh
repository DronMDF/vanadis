#!/bin/sh
set -e
if [ "${DATABASE}" = "postgresql" ]; then
	echo "PostgreSQL database..."
	apt-get -y install postgresql python3-psycopg2
	service postgresql start
	runuser -u postgres -- psql -c "create role vanadis with login createdb password 'vanadis';"
	runuser -u postgres -- psql -c "create database vanadisdb;"
else
	echo "Sqlite database..."
fi
