# -*- coding: utf-8 -*-
#  File: full_update_db.py
#  Project: 'Bookmarks search'
#  Created by Gennady Matveev (gm@og.ly) on 05-12-2021.
#  Copyright 2021. All rights reserved.

# %%
# Import libraries

import os
import json
import pandas as pd
import streamlit as st
import pickle
import fasttext
import warnings
from parse_json import *
from df_from_json import *
from df_to_sql import *
from scrape import *
from helpers import *

warnings.filterwarnings('ignore')

# %%
# JSON PARSING PART BEGIN ======================================================
# Turn JSON into list of lists


def json_to_list() -> list:

    # Read Bookmarks file into JSON
    bookmarks_path = st.secrets["bookmarks_path"]['path']

    with open(bookmarks_path, 'r') as json_file:
        data = json.loads(json_file.read())

    json_list = get_json_list(data)

# Clean meta_info records
    [json_list.remove(row) for row in json_list if pt(
        row, -1) == 'last_visited_desktop']

# Read JSON into dataframe
    df = pd.DataFrame()
    df = (df.pipe(
        start_pipeline, json_list)
        .pipe(fill_df, json_list)
        .pipe(clean_df)
    )

# Save df to pickle
    with open('./data/df_.pickle', 'wb') as p:
        pickle.dump(df, p)

# Save json_list depth to pickle
    with open('./data/json_list_depth.pickle', 'wb') as q:
        pickle.dump(list_depth(json_list), q)

    return df
    # return df[:5]

# JSON PARSING PART END ========================================================

# %%
# NEW BOOKMARKS PART BEGIN =====================================================
# check dfn guid against database guid


def new_bookmarks(df: pd.DataFrame) -> pd.DataFrame:
    query = 'SELECT guid FROM bookmarks'
    conn = connect()

# Retrieve existing guids from SQL database
    dfx = pd.DataFrame()
    dfx = pd.read_sql(query, conn, columns=['guid'])
    guids = dfx['guid'].to_list()

# Select newly added bookmarks
    dfn = df.loc[~df['guid'].isin(guids)]
    print(f'Inserting {dfn.shape[0]} new record(s)')
    return dfn

# NEW BOOKMARKS PART END =======================================================
# %%
# SCRAPING PART BEGIN ==========================================================


def scrape_to_sql(dfn: pd.DataFrame) -> str: 
    
    fasttext.FastText.eprint = lambda x: None
    model = fasttext.load_model('./data/lid.176.ftz')

    headers = {'User-Agent': st.secrets["user_agent"]["agent"]}

# Scrape only new bookmarks

    if dfn.shape[0] > 0:
        dfn = scraper(dfn, model=model, headers=headers)
        print('Scraping completed')


# SCRAPING PART END ============================================================

# SQLite PART BEGIN ============================================================

# Insert new bookmarks into SQL database
        conn = connect()
        
        execute_sql_batch(conn, dfn)

        print("Database update completed")
        os.system('afplay ./sounds/eagle_has_landed.mov')

        conn.close()
    else:
        os.system('afplay ./sounds/no_hooch.mov')
        print('No new bookmarks')
    
    # return status

# SQLite PART END ==============================================================

# %%

def part_update(): 
    df = json_to_list()
    # Save df to pickle
    with open('./data/df.pickle', 'wb') as p:
        pickle.dump(df, p)
    dfn = new_bookmarks(df)
    scrape_to_sql(dfn)

# %%
