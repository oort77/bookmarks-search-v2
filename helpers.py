# -*- coding: utf-8 -*-
#  File: helpers.py
#  Project: 'Bookmarks search'
#  Created by Gennady Matveev (gm@og.ly) on 05-12-2021.
#  Copyright 2021. All rights reserved.

#%%
# Import libraries

from datetime import datetime, timedelta
import re
import tomli
import warnings

warnings.filterwarnings('ignore')

# Helper functions

def pt(r , n: int) -> str:
    return str.split(r[0], '.')[n]


def stem(r, len: int) -> str:
    return str.rsplit(r[0], '.', len)[0]


def fetch_val(st:str, lst): #: str : list
    for x in lst:
        if x[0] == st and len(x) > 1:
            return x[1]


def list_depth(lst: list) -> int: #m: int=0
    m = 0
    for row in lst:
        if ((len(str.split(row[0], '.')) > m)):
            m += 1
    return m - 1

def black_list() -> list:
    """
    Fetches list of bad domains.
    """
    with open("./black_list.toml", "rb") as f:
        return tomli.load(f)['blacklist']


def exclude_blacklisted_domain(url: str) -> bool:#, blacklist: list=blacklist) -> bool:
    """
    Returns True if url is not in the blacklist.
    """
    m = re.search('https?://([A-Za-z_0-9.-]+).*', url)
    return m.group(1) not in black_list()


def getFiletime(dtms: int) -> str:
    seconds, _ = divmod(dtms, 1000000)
    days, seconds = divmod(seconds, 86400)
    dt = datetime(1601, 1, 1) + timedelta(days, seconds)  # , micros)
    return dt.strftime("%-d %b %Y") # %H:%M
