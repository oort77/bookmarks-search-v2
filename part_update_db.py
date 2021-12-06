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

#%%
# Read Bookmarks file into JSON
bookmarks_path = '/users/gm/Library/Application \
Support/BraveSoftware/Brave-Browser/Default/Bookmarks'

with open(bookmarks_path, 'r') as json_file:
    data = json.loads(json_file.read())
# %%
# JSON PARSING PART BEGIN ======================================================

# Turn JSON into list of lists
json_list = get_json_list(data)

# Clean meta_info records
[json_list.remove(row) for row in json_list if pt(
    row, -1) == 'last_visited_desktop']

# Read JSON into dataframe
df = pd.DataFrame()
df = (df.pipe(
    start_pipeline, json_list)
    .pipe(fill_df, json_list)
    .pipe(clean_df))

# Save df to pickle
with open('./data/df_.pickle', 'wb') as p:
    pickle.dump(df, p)

# Save json_list depth to pickle
with open('./data/json_list_depth.pickle', 'wb') as q:
    pickle.dump(list_depth(json_list), q)


# JSON PARSING PART END ========================================================

# %%
# TESTING PART BEGIN ===========================================================

# df = df[:5]

# TESTING PART END =============================================================

# %%
# NEW BOOKMARKS PART BEGIN =====================================================
# check dfn guid against database guid

query = 'SELECT guid FROM bookmarks'
conn = connect()

# Retrieve existing guids from SQL database
dfx = pd.DataFrame()
dfx = pd.read_sql(query,conn,columns=['guid'])
guids = dfx['guid'].to_list()

# Select newly added bookmarks
dfn = df.loc[~df['guid'].isin(guids)]
print(f'\nPreparing to insert {dfn.shape[0]} new records...\n')

# NEW BOOKMARKS PART END =======================================================
# %%
# SCRAPING PART BEGIN ==========================================================
fasttext.FastText.eprint = lambda x: None
model = fasttext.load_model('./data/lid.176.ftz')
headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
# Scrape only new bookmarks

if dfn.shape[0] > 0:
    dfn = scraper(dfn, model=model, headers=headers)
    print('\nScraping completed...\n')

# Save df to pickle
    with open('./data/df.pickle', 'wb') as p:
        pickle.dump(df, p)
        
# SCRAPING PART END ============================================================

# SQLite PART BEGIN ============================================================

# Insert new bookmarks into SQL database

    print('Connecting to the PostgreSQL database...')
    conn = connect()
    print("\nConnection successful")

    execute_batch(conn, dfn)

    print("\nDatabase update completed...\n")
    os.system('afplay ./sounds/eagle_has_landed.mov')

    conn.close()
else:
    os.system("say 'Velma you says? No new bookmarks, no hooch, no gals no nothing... Just the scram white boy, just scram'")
    print('\nNo new bookmarks since last update\n')
    
# SQLite PART END ==============================================================
# %%
