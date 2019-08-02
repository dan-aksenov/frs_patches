# for postgresql connection
from psycopg2 import connect

def postgres_exec(db_host, db_name, sql_query):
    ''' SQL execution '''

    # pgpass shoule be used insead of password
    conn_string = 'dbname= ' + db_name + ' user=''postgres'' host=' + db_host
    try:
        conn = connect(conn_string)
    except:
        print( Bcolors.FAIL + "\nERROR: unable to connect to the database!" + Bcolors.ENDC )
        sys.exit()
    cur = conn.cursor()
    cur.execute(sql_query)
    query_results = []
    # This check needed, because delete doesn't return cursor
    if cur.description is not None:
        rows = cur.fetchall()
        # Need list of stings instead of tuples for future manipulation.
        for row in rows:
            query_results.append(row[0])
    rowcnt = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return query_results, rowcnt
