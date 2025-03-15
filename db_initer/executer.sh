#!/bin/bash

DB_HOST=postgres

while ! pg_isready -q -U ${PGUSER} -h ${DB_HOST} -d postgres ; do
    echo "Waiting for server to start..."
    sleep 2
done
echo "Server is ready..."

psql -U ${PGUSER} -h ${DB_HOST} -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '${PGDATABASE}'" | grep -q 1 || \
psql -U ${PGUSER} -h ${DB_HOST} -d postgres -c "CREATE DATABASE ${PGDATABASE}"

echo "Database is ready"

psql -U ${PGUSER} -h ${DB_HOST} -d ${PGDATABASE} -f /db_initer/table_create.sql

echo "Table is ready"
