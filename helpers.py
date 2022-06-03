# -*- coding: utf-8 -*-
#  File: helpers.py
#  Project: 'Bookmarks search'
#  Created by Gennady Matveev (gm@og.ly) on 05-12-2021.
#  Copyright 2021. All rights reserved.

# %%
# Import libraries

from datetime import datetime, timedelta
import re
import tomli
import warnings

from contextlib import contextmanager
from io import StringIO
from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from threading import current_thread
import streamlit as st
import sys
from time import sleep

warnings.filterwarnings('ignore')

# Helper functions


def pt(r, n: int) -> str:
    return str.split(r[0], '.')[n]


def stem(r, len: int) -> str:
    return str.rsplit(r[0], '.', len)[0]


def fetch_val(st: str, lst):  
    for x in lst:
        if x[0] == st and len(x) > 1:
            return x[1]


def list_depth(lst: list) -> int: 
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


def exclude_blacklisted_domain(url: str) -> bool:
    """
    Returns True if url is not in the blacklist.
    """
    m = re.search('https?://([A-Za-z_0-9.-]+).*', url)
    return m.group(1) not in black_list()


def getFiletime(dtms: int) -> str:
    seconds, _ = divmod(dtms, 1000000)
    days, seconds = divmod(seconds, 86400)
    dt = datetime(1601, 1, 1) + timedelta(days, seconds)
    return dt.strftime("%-d %b %Y")


# Redirect sys.stdout to streamlit sidebar
@contextmanager
def st_redirect(src, dst):
    placeholder = st.sidebar.empty()
    output_func = getattr(placeholder, dst)

    with StringIO() as buffer:
        old_write = src.write

        
        def new_write(b):
            if getattr(current_thread(), REPORT_CONTEXT_ATTR_NAME, None):
                buffer.write(b)
                sleep(1)
                buffer.seek(0)
                output_func(b)  # Changed here
                # output_func(buffer.read())
                
            else:
                old_write(b)
            # sys.stdout.write(b)

        try:
            src.write = new_write

            yield
            
        finally:
            src.write = old_write

    placeholder.empty()

@contextmanager
def st_stdout(dst):
    with st_redirect(sys.stdout, dst):
        yield


@contextmanager
def st_stderr(dst):
    with st_redirect(sys.stderr, dst):
        yield
