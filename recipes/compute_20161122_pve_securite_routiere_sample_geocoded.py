# -*- coding: utf-8 -*-
import dataiku as d
import os.path
import codecs, io, StringIO, requests
import pandas as pd, numpy as np
import concurrent.futures
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
    return df


# Recipe inputs
f = d.Dataset("20161122_pve_securite_routiere_sample")
liste=[]
split=500
nthreads=2
i=0

#version monothread
#for events_subset in f.iter_dataframes(chunksize=split):
#    i+=split
#    print("Enrichissement addok/BAN: {}...".format(i))
#    liste.append(adresse_submit(events_subset))
#    # Insert here applicative logic on each partial dataframe.
#    pass    

#multithread
with concurrent.futures.ThreadPoolExecutor(max_workers=nthreads) as executor:
    enrich={executor.submit(adresse_submit,subset): subset for subset in f.iter_dataframes(chunksize=split)}
    for subset in concurrent.futures.as_completed(enrich):  
        i+=split
        subset=enrich[subset]
        try:
            liste.append(subset)
        except Exception as exc:
            print ("chunk %r to %r generated an exception: %s\n%r" %(i-split,i,exc,subset))
        else:
            print("geocoded chunk %r to %r" %(i-split,i))



events=pd.concat(liste,ignore_index=True)

# Recipe outputs
out = d.Dataset("20161122_pve_securite_routiere_sample_geocoded")
out.write_with_schema(events)
