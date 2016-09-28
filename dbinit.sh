#!/bin/sh

if [ "${DATABASE}" = "postgresql" ]; then
	echo "PostgreSQL database..."
	pip install psycopg2
	psql -c "create role vanadis with login createdb password 'vanadis';" -U postgres
	psql -c "create database vanadisdb;" -U postgres
else
	echo "Sqlite database..."
fi
