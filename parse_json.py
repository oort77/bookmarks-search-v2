# -*- coding: utf-8 -*-
#  File: parse_json.py
#  Project: 'Bookmarks search'
#  Created by Gennady Matveev (gm@og.ly) on 05-12-2021.
#  Copyright 2021. All rights reserved.

# %%
# Import libraries

import warnings

warnings.filterwarnings('ignore')

def get_json_list(lst) -> list:
    global g
    g = []
    return get_list(lst)

def get_list(v: dict, prefix: str ='x') -> list: 
    """
    Turns JSON data string into list of lists
    """
    global g
    
    if isinstance(v, dict):
        for k, v2 in v.items():
            p2 = "{}.{}".format(prefix, k)
            get_list(v2, p2)  # recursive call

    elif isinstance(v, list):
        for i, v2 in enumerate(v):
            p2 = "{}{}".format(prefix, i)
            get_list(v2, p2)  # recursive call
    else:
        g.append(['{}'.format(prefix), v])

    return g
