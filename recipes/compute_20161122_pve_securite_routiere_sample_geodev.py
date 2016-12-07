# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Recipe inputs
in_ds = dataiku.Dataset("20161122_pve_securite_routiere_sample_geocoded")
in_df = in_ds.get_dataframe()

out_df = in_df.unstack(level=1)

# Recipe outputs
out_ds = dataiku.Dataset("20161122_pve_securite_routiere_sample_geodev")
out_ds.write_with_schema(out_df)
