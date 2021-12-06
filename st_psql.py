# -*- coding: utf-8 -*-
#  File: st_psql.py
#  Project: 'Chrome bookmarks'
#  Created by Gennady Matveev (gm@og.ly) on 05-12-2021.
#  Copyright 2021. All rights reserved.

# %%
# Import libraries

import os
from datetime import datetime
import streamlit as st
import pickle
import fasttext
from df_to_sql import *
from helpers import *

# Load language recognition model
model = fasttext.load_model('./data/lid.176.ftz')
fasttext.FastText.eprint = lambda x: None

# STREAMLIT PART BEGIN =========================================================

# Init srteamlit
st.set_page_config(page_title='Brave bookmarks search',
                   page_icon='images/icon_search.ico',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.image('./images/header.png')
# %%

# Set up input for search language and output format in sidebar
ru_search = st.sidebar.checkbox('Search in Russian')

# Choose the number of search results
num_res = st.sidebar.number_input(
    'Number of results', min_value=5, value=25, step=5, format='%i')

# Choose the number of characters in snippet string
num_chars = st.sidebar.number_input(
    'Number of characters in text', min_value=100, value=500,
    step=100, format='%i')

# Vertical spacing in sidebar
st.sidebar.markdown('<hr>', unsafe_allow_html=True)
st.sidebar.image('./images/filler.png', use_column_width=True)

# Display last updated info
with open('./data/last_updated.pickle','rb') as f:
    last_updated = pickle.load(f)
date_last_updated = last_updated.strftime('%-d %b %Y')
st.sidebar.write(f'Last updated on {date_last_updated}')

# Database update widgets
full_update = st.sidebar.checkbox('Full update')
update_db = st.sidebar.button(
    'Update database', help='Update may take a while')

# Set up input field for search phrase
search_text = st.text_input(label='')

# Predict search text language
lang_search_text = model.predict(search_text)[0][0].rsplit('__', 1)[1]

# Check search language
language = 'russian' if ru_search else 'english'

# Override English if search text is in Russian
if language == 'english' and lang_search_text == 'ru':
    language = 'russian'
st.write(f'Search language is **{language.capitalize()}**')

# Replace single quotes with double in search string
for char in search_text:
    if (char == "'" or char == '"'):
        search_text = search_text.replace(char, '"')
# STREAMLIT PART END ===========================================================

# %%
# SQL PART BEGIN ===============================================================

# Prepare search query
# Load json_list depth from pickle
with open('./data/json_list_depth.pickle', 'rb') as f:
    depth = pickle.load(f)
# Change to range(depth-6, depth-3) to see the last subfolder as well // folder2, folder3
folders_list = ['folder' + str(i) for i in range(depth-6, depth-4)] 
folders = ', '.join(folders_list)

search_query = f"""
                SELECT date_added, url, name,  
                ts_rank_cd( 
                    to_tsvector('{language}', body), 
                    websearch_to_tsquery('{language}', '{search_text}'), 
                    32 
                    ) AS rank, 
                ts_headline('{language}', body,
                    websearch_to_tsquery('{language}', '{search_text}'),
                    'MaxFragments=8, MaxWords=100, MinWords=5, 
                    StartSel=<b>, StopSel=</b>'), 
                    {folders}
                FROM bookmarks  
                WHERE websearch_to_tsquery('{language}', '{search_text}') 
                    @@ to_tsvector('{language}', body) 
                ORDER BY rank DESC 
                LIMIT {num_res};
                """
# %%
# Connect to the PostgreSQL database server

conn = connect()

# Render search result
spacer = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'


def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


try:
    rows = run_query(search_query)
    conn.commit()

    if search_text != '' and len(rows) == 0:
        st.error('No results found')

    for row in rows:
# TODO: make field count dependent of json_list depth
        st.markdown(f'**{row[2]}** <br>[{row[1]}]({row[1]})  \
                    <br>Rank {round(row[3]*100)}{spacer}  \
                    Added on {getFiletime(row[0])}{spacer}  \
                    Tags:&nbsp;&nbsp;{row[depth-3]}  >  {row[depth-2]}', unsafe_allow_html=True)

        st.markdown(f'{row[4][:num_chars]}<hr>', unsafe_allow_html=True)

except Exception as error:
    st.error(f"Error: %s" % error)
    conn.rollback()

# SQL PART END =================================================================

# %%
# DATABASE UPDATE PART BEGIN ===================================================

if update_db:
    
    os.system('afplay ./sounds/gagarin_poehali.mov')

    if full_update:
        print('\n\nStarting full database update...')
        os.system("python full_update_db.py &")
    else:
        os.system("python part_update_db.py &")
        print('\nStarting partial database update...')
    # Save update time to pickle    
    last_updated = datetime.now()
    with open('./data/last_updated.pickle','wb') as f:
        pickle.dump(last_updated, f)


# DATABASE UPDATE PART END =====================================================

# %%
