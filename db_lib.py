import sqlite3
from sqlite3 import Error
import os.path
import pandas as pd 

from utils import *

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def select_all_rows(conn,table_name):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :param table_name: table name
    :return: rows of a table 
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table_name)

    rows = cur.fetchall()

    return rows

def select_all_files(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return: rows of a table 
    """
    cur = conn.cursor()
    cur.execute("SELECT distinct file_generation_number FROM files ")

    rows = cur.fetchall()

    return rows


def delete_records(conn,where_clause):
    """
    Update db for duplciate records
    :param conn: the Connection object
    :param where clause: records to be deleted 
    :return:
    """
    try:
        c = conn.cursor()
        c.execute("DELETE FROM timeseries WHERE " + where_clause)
    except Error as e:
        print(e)

def overview_report(conn):
    """
    Return specific report 
    :param conn: the Connection object
    :param date: the date for the report to be ran 
    :return: tuple to be used for the result 
    """

    sql_report_query1 = """     SELECT count(distinct meter_number ) as meters 
                                ,count(distinct file_name) as items
                                FROM timeseries 

                         """ 

    cur1 = conn.cursor()
    cur1.execute(sql_report_query1)
    rows = cur1.fetchall()

    return rows[0]

def last_file_report(conn):
    """
    Return specific report 
    :param conn: the Connection object
    :param date: the date for the report to be ran 
    :return: tuple to be used for the result 
    """

    sql_report_query1 = """     SELECT distinct file_generation_number, time_stamp
                                FROM files as f
                                inner join (
                                    SELECT max(time_stamp) as max_ts 
                                    from files
                                ) as mf
                                on mf.max_ts = f.time_stamp

                         """ 

    cur1 = conn.cursor()
    cur1.execute(sql_report_query1)
    rows = cur1.fetchall()

    return rows[0]

def meter_data(conn,meter_number):
    """
    Return specific report 
    :param conn: the Connection object
    :param date: the date for the report to be ran 
    :return: tuple to be used for the result 
    """

    sql_report_query1 = """     SELECT * 
                                FROM timeseries
                                WHERE meter_number = """ + str(meter_number) + """
                         """ 

    cur1 = conn.cursor()
    cur1.execute(sql_report_query1)
    rows = cur1.fetchall()

    return rows

def main(database):
    
    sql_create_files_table = """ CREATE TABLE IF NOT EXISTS files (
                                        id integer PRIMARY KEY,
                                        record_identifier text NOT NULL,
                                        file_type_identifier text NOT NULL, 
                                        company_id text NOT NULL, 
                                        file_creation_date text NOT NULL, 
                                        file_creation_time text NOT NULL, 
                                        file_generation_number text NOT NULL,
                                        time_stamp text NOT NULL
                                    ); """

    sql_create_timeseries_table = """ CREATE TABLE IF NOT EXISTS timeseries (
                                        id integer PRIMARY KEY,
                                        record_identifier text NOT NULL,
                                        meter_number text NOT NULL, 
                                        measurement_date text NOT NULL, 
                                        measurement_time  text NOT NULL, 
                                        consumption text NOT NULL,
                                        file_name text NOT NULL
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_files_table)

        # create tasks table
        create_table(conn, sql_create_timeseries_table)

        # return connection to the database 
        return conn

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()