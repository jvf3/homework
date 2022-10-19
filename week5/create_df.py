import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randint(0,100,size=(1000000, 4)), columns=list('ABCD'))
df['E'] = df['D']


