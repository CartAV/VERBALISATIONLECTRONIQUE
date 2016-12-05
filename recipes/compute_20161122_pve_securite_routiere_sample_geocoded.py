# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Recipe inputs
20161122_pve_securite_routiere_sample = dataiku.Dataset("20161122_pve_securite_routiere_sample.csv")
20161122_pve_securite_routiere_sample_df = 20161122_pve_securite_routiere_sample.get_dataframe()



# Recipe outputs
20161122_pve_securite_routiere_sample_geocoded = dataiku.Dataset("20161122_pve_securite_routiere_sample_geocoded")
20161122_pve_securite_routiere_sample_geocoded.write_with_schema(pandas_dataframe)
