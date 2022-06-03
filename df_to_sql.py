# -*- coding: utf-8 -*-
#  File: df_to_sql.py
#  Project: 'Bookmarks search'
#  Created by Gennady Matveev (gm@og.ly) on 05-12-2021.
#  Copyright 2021. All rights reserved.

# %%
# Import libraries

import pandas as pd
import psycopg2
import psycopg2.extras as extras
import streamlit as st
import sys

#%%
# SQL PART =====================================================================

# Establish connection to SQL db

def connect():
    
    conn = None
    try:
        # connect to the PostgreSQL server
        # conn = psycopg2.connect(**params_dic)
        conn = psycopg2.connect(**st.secrets["postgres"])

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)

    return conn


# %%
# Insert df in SQL db


def execute_sql_batch(conn, df: pd.DataFrame, page_size: int = 100)->str: #status: str,
    
    # Create a list of tuples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]

    db_cols = df.columns
    
    # SQL query to execute

    query = f"""
            INSERT INTO bookmarks({', '.join(db_cols)}) VALUES 
                    ({', '.join(['%s']*len(db_cols))}) 
            ON CONFLICT (guid) DO NOTHING
            """
    cur = conn.cursor()
    
    try:
        extras.execute_batch(cur, query, tuples, page_size)
        conn.commit()
        # status = 'Update completed'
        print('SQL batch Update completed')
        # print(f'df_to_sql status = {status}')

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        # status = 'Update failed'
        print('Update failed')

    # print("Dataframe fetched to SQL")

    cur.close()

    # return status
# END SQL PART =================================================================

# %%
