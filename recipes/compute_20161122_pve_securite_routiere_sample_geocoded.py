# -*- coding: utf-8 -*-
import dataiku as d
import os.path
import codecs, io, StringIO, requests
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from collections import OrderedDict

def adresse_submit(df):
    s = StringIO.StringIO()
    df.to_csv(s,sep=",", quotechar='"',encoding="utf8",index=False)
    requests_session = requests.Session()
    kwargs = {
        'data': OrderedDict([
                ('columns', 'VOIE_INFRACTION'), 
                ('citycode', 'CODE_INSEE_INFRACTION'),
               ('encoding','utf8')
        ]),
        'method': 'post',
        'files': OrderedDict([
            ('data', s.getvalue())
        ]),
        'stream': True,
        'timeout':500,
        'url': 'http://fa-srv-1/search/csv/'
    }
    response = requests_session.request(**kwargs)
    df=pd.read_csv(StringIO.StringIO(response.content.decode('utf-8')),sep=",",quotechar='"')
    return response.content


# Recipe inputs
f = d.Dataset("20161122_pve_securite_routiere_sample")
liste=[]
split=500
i=0

for events_subset in f.iter_dataframes(chunksize=split):
    i+=split
    print("Enrichissement addok/BAN: {}...".format(i))
    events=pd.read_csv(adresse_submit(events_subset),",",encoding="utf8",quotechar='"')
    # Insert here applicative logic on each partial dataframe.
    pass    

#events=pd.concat(liste,ignore_index=True)

# Recipe outputs
out = d.Dataset("20161122_pve_securite_routiere_sample_geocoded")
out.write_with_schema(events)
