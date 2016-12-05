# -*- coding: utf-8 -*-
import dataiku as d
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Recipe inputs
f = d.Dataset("20161122_pve_securite_routiere_sample")
events = f.get_dataframe()



# Recipe outputs
out = d.Dataset("20161122_pve_securite_routiere_sample_geocoded")
out.write_with_schema(pandas_dataframe)
