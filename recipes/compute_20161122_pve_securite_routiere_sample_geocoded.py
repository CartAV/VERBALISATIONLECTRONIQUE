# -*- coding: utf-8 -*-
import dataiku as d
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

step=1000


def 

# Recipe inputs
f = d.Dataset("20161122_pve_securite_routiere_sample")
events = f.get_dataframe()

#splitting
for k in range(step,len(events)+step,step):
    file="tmp_{}".format(k)
    events[k-step:k].to_csv(file,sep=";",quotechar='"',index=false)
    

# Recipe outputs
out = d.Dataset("20161122_pve_securite_routiere_sample_geocoded")
out.write_with_schema(events)
