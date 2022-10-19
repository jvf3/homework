import numpy as np
import pandas as pd
import pyarrow.feather as feather


df = pd.DataFrame(np.random.randint(0,100,size=(1000000, 4)), columns=list('ABCD'))
df['E'] = df['D']
%time df.to_csv("./abcde.csv")
%time df.to_hdf("./abcde.h5", key="Rand")
%time df.to_pickle("./abcde.pkl")
%time feather.write_feather(df,"./abcde.arrow")
%time df.to_parquet("./abcde.parquet")
