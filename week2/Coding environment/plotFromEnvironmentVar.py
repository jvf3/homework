# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 15:26:07 2022

@author: angel
"""

import pandas as pd
import os

path = os.environ['RESEARCH_PATH']
#or if manually setting environment variable in python
# RESEARCH_PATH  = r'C:\Users\angel\OneDrive\Desktop\MQF\Fall 2022\Digital Tools\duangel\homework'
df = pd.read_csv(path + '\coding-environment-exercise.csv')
df['date'] =  pd.to_datetime(df['date'], format='%Y-%m-%d')
df = df.set_index('date')

# Plot
df.plot()
