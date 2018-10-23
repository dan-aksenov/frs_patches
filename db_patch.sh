#Set database's host from first parameter.
PGHOST=$1

PGPORT=5432
PGUSER=$3
#should be in .pgpass
#set PGPASSWORD=ods

#Set database name from second parameter
PGDATABASE=$2

# Install patch
psql -f intall.sql &>install.log