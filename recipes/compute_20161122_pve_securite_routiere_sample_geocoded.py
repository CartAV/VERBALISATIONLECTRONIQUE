# -*- coding: utf-8 -*-
import dataiku as d
import os.path
import codec, io, StringIO, requests
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from collections import OrderedDict

def adresse_submit(file):
    requests_session = requests.Session()
    print("Enrichissement addok/BAN: {}...".format(file))
    kwargs = {
        'data': OrderedDict([
            ('columns', 'VOIE_INFRACTION'), 
            ('citycode', 'CODE_INSEE_INFRACTION')
        ]),
        'method': 'post',
        'files': OrderedDict([
            ('data', (file,
                      io.BytesIO(
                          open(file, 'rb').read()
                    )))
        ]),
        'stream': True,
        'timeout':500,
        'url': 'http://fa-srv-1/search/csv/'
    }
    response = requests_session.request(**kwargs)
    with codecs.open(file+"geo", 'wb', 'utf8') as f:
        f.write(response.text)
    return True;


# Recipe inputs
f = d.Dataset("20161122_pve_securite_routiere_sample")
liste=[]

for events_subset in f.iter_dataframes(chunksize=500):
    events_subset.to_csv("tmp.csv",sep=";", quotechar='"',index=False)
    adresse_submit("tmp.csv")
    liste.append(pd.read_csv("tmp.csvgeo",sep=";", na_filter=False,dtype=object,index_col=None))
    # Insert here applicative logic on each partial dataframe.
    pass    
events=pd.concat(liste,ignore_index=True)

# Recipe outputs
out = d.Dataset("20161122_pve_securite_routiere_sample_geocoded")
out.write_with_schema(events)
