# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Recipe inputs
ds_in = dataiku.Dataset("20161122_pve_securite_routiere_sample_geocoded")
df = ds_in.get_dataframe()

df=pd.concat([df,pd.get_dummies(df['GENRE'])],axis=1)


# Recipe outputs
ds_out = dataiku.Dataset("20161122_pve_securite_routiere_sample_geo_dum")
ds_out.write_with_schema(df)
