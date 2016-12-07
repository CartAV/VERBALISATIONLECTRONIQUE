# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Recipe inputs
ds_in = dataiku.Dataset("20161122_pve_securite_routiere_sample_geocoded")
df = ds_in.get_dataframe()

nrows=df.count+1
thresold=0.02*float(nrows)

liste=('REGROUPEMENT_GENRE','LIBELLE_CLASSE','SEXE_CONTREVENANT','LIBELLE_FAMILLE')
for key in liste:
    values = df[key]
    counts = pd.value_counts(values)
    mask = values.isin(counts[counts > int(threshold)].index)
    df=pd.concat([df,pd.get_dummies(values[mask],prefix=key,prefix_sep=" ")],axis=1)

    

# Recipe outputs
ds_out = dataiku.Dataset("20161122_pve_securite_routiere_sample_geo_dum")
ds_out.write_with_schema(df)
