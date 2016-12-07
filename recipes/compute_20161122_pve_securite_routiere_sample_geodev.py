# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Recipe inputs
20161122_pve_securite_routiere_sample_geocoded = dataiku.Dataset("20161122_pve_securite_routiere_sample_geocoded")
df = 20161122_pve_securite_routiere_sample_geocoded.get_dataframe()

out = df.unstack(level=1)

# Recipe outputs
20161122_pve_securite_routiere_sample_geodev = dataiku.Dataset("20161122_pve_securite_routiere_sample_geodev")
20161122_pve_securite_routiere_sample_geodev.write_with_schema(out)
