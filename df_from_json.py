# -*- coding: utf-8 -*-
#  File: df_from_json.py
#  Project: 'Bookmarks search'
#  Created by Gennady Matveev (gm@og.ly) on 05-12-2021.
#  Copyright 2021. All rights reserved.
# %%
# Import libraries

from parse_json import *
import pandas as pd
import warnings
from helpers import *

warnings.filterwarnings('ignore')

# Set up pandas pipeline


def start_pipeline(dataf: pd.DataFrame, json_list: list) -> pd.DataFrame:  # = json_list
    perm_cols = ['date_added', 'guid', 'name', 'url', 'body', 'lang']
    folder_cols = ['folder' + str(i) for i in range(list_depth(json_list) - 3)]
    cols = perm_cols + folder_cols
    dataf = pd.DataFrame(columns=cols)
    print('\nPipeline started...')
    return dataf


def fill_df(dataf: pd.DataFrame, json_list: list) -> pd.DataFrame:  # = json_list
    perm_cols = ['date_added', 'guid', 'name', 'url', 'body', 'lang']
    for i, s in enumerate(json_list):
        if pt(s, -1) == 'type' and s[1] == 'url':
            l = len(str.split(s[0], '.'))
            for col in dataf[perm_cols].columns:
                dataf.loc[i, col] = fetch_val(stem(s, 1) + "."+col, json_list)
            for fn in range(list_depth(json_list) - 3):
                dataf.loc[i, 'folder'+str(fn)] = fetch_val(stem(s, l - fn-3) + '.name', json_list) if (
                    fetch_val(stem(s, l - fn - 3) + '.type', json_list) != 'url') else None
    print('Dataframe filled...')
    return dataf


def clean_df(dataf: pd.DataFrame) -> pd.DataFrame:
    # Shorten page name
    dataf['name'] = dataf['name'].apply(lambda x: x[:250])
    # Ignore non-http urls
    dataf = dataf.loc[dataf['url'].str.startswith('http')]
    # Use urls_black_list to block problematic or unneeded urls
    # blacklist = black_list()
    dataf = dataf.loc[dataf['url'].apply(exclude_blacklisted_domain)]
    # Reset index
    dataf.reset_index(drop=True, inplace=True)
    print('Dataframe cleaned...\n')
    return dataf
