import csv
from io import StringIO
import logging

from sqlalchemy import create_engine

logger = logging.getLogger(__name__)



def _psql_insert_copy(table, conn, keys, data_iter):
    """
    """
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)
        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '"{}"."{}"'.format(table.schema, table.name)
        else:
            table_name = table.name
        sql = "COPY {} ({}) FROM STDIN WITH CSV".format(table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

def _table_exists(engine, schema, table):
    with engine.connect() as conn:
        sql = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s
            AND table_name = %s;
        """
        return conn.execute(sql, schema, table).rowcount

def _truncate_table(engine, schema, table):
    with engine.connect() as conn:
        sql = f"""
            TRUNCATE TABLE "{schema}"."{table}";
        """
        conn.execute(sql)

def load_to_table(df, dest, pg_conn_cred, timeout=600000):
    schema, table = dest.split(".")
    engine = create_engine(pg_conn_cred)
    if _table_exists(engine, schema, table):
        _truncate_table(engine, schema, table)
        if_exists = "append"
    else:
        if_exists = "fail"

    # load data
    with engine.connect() as conn:
        conn.execute(f"SET statement_timeout = {timeout};")
        df.to_sql(table, conn, schema, if_exists=if_exists, 
        index=False, 
        method=_psql_insert_copy
        )
