#!/usr/bin/python

import psycopg2
import pandas as pd
from src.dash.config import Configuration


class PostgresTasks:
    config = Configuration()

    def psql_to_df(self, table_name:str, column_names:list[str], additional_operations: str= None) -> pd.DataFrame:
        """select data from   PostgreSQL database (database specified in config.py), 
        table_name: table to select from
        column_names: list of columns to select
        additional_operations: further commands for the PostgreSQL query (i.e. "ORDER BY time DESC LIMIT 10000")
        """
        command = f"SELECT {', '.join(column_names} FROM {table_name}"
        if additional_operations:
        	       command = f"SELECT {', '.join(column_names} FROM {table_name} {additional_operations}"
        conn = None
        try:
            # read the connection parameters
            params = PostgresTasks.config.postgresql_config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table one by one
            cur.execute(command)
            #fetch the data
            data_from_psql = cur.fetchall()
            # close communication with the PostgreSQL database server
            cur.close()

        except (psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return pd.DataFrame(data= data_from_psql, columns = column_names)

# to test a specific function via "python postgresql_tasks.py" in the powershell
if __name__ == "__main__":
    postgres_task = PostgresTasks()
    postgres_task.psql_to_df("nibe", [data_id, time, momentan_verwendete_leistung, brauchwasser_nur_verdichter, heizung_nur_verdichter])
#