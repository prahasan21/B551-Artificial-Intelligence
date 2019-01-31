# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 23:08:24 2018

@author: 18123
"""
import numpy as np
from astropy.io import ascii
from astropy.table import Table

data = Table({'BFS': [1, 2, 3],'DFS': [1, 2, 3],'IDS':[1,2,3],'A*':[1,2,3]},names=['BFS','DFS','IDS', 'A*'])
ascii.write(data)