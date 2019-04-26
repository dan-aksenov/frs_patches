#!/bin/bash
# Set database's host from first parameter.
PGHOST=$1

PGPORT=5432
PGUSER=$3
# password should be in .pgpass

# Set database name from second parameter
PGDATABASE=$2

# Install patch
psql -h $1 -U $3 -f install_db.sql $2 &>install_db_log.log
