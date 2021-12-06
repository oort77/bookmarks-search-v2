# -*- coding: utf-8 -*-
#  File: scrape.py
#  Project: 'Bookmarks search'
#  Created by Gennady Matveev (gm@og.ly) on 05-12-2021.
#  Copyright 2021. All rights reserved.

# %%
# Import libraries

import time
import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
import requests
import re
import warnings

warnings.filterwarnings('ignore')

headers = {'User-Agent': st.secrets["user_agent"]}

def get_txt(url:str, headers: dict):
    try:
        HTML = requests.get(url, headers=headers)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        t = re.sub(r"\s+", " ", soup.get_text())
        # .decode("utf-8", errors="replace")
        text = t.replace("\x00", "\uFFFD")

    except requests.ConnectionError as exception:
        print(f'Connection error! \n {exception}')
        text = ''
    return text


def scraper(dataf: pd.DataFrame, model, headers: dict) -> pd.DataFrame:
    counter = 0
    for _, row in dataf.iterrows():
        if pd.isna(row['body']):
            row['body'] = get_txt(row['url'], headers)[:1000000]
            lang = model.predict(row['body'], k=1)[0][0][-2:]
            row['lang'] = 'russian' if lang == 'ru' else 'english'
            time.sleep(0.3)
            counter += 1
            print(counter, row['url'][:50])
    return dataf

# %%
