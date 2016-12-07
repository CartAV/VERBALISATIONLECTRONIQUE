# -*- coding: utf-8 -*-
import dataiku as d
import os.path
import codecs, io, StringIO, requests
import pandas as pd, numpy as np
import concurrent.futures
from dataiku import pandasutils as pdu
from collections import OrderedDict

# Recipe inputs
f = d.Dataset("20161122_pve_securite_routiere_sample")
i=0
liste=[]
futures=[]
split=1
verbosechunksize=1000
maxtries=3
nthreads=8
j=0

def adresse_submit(df):
    global i
    s = StringIO.StringIO()
    i+=split
    df.to_csv(s,sep=",", quotechar='"',encoding="utf8",index=False)
    requests_session = requests.Session()
    kwargs = {
        'data': OrderedDict([
                ('columns', 'VOIE_INFRACTION'), 
                ('citycode', 'CODE_INSEE_INFRACTION')
        ]),
        'method': 'post',
        'files': OrderedDict([
            ('data', s.getvalue())
        ]),
        'stream': True,
        'timeout':500,
        'url': 'http://fa-srv-1/search/csv/'
    }
    if ((i%verbosechunksize)==0):
        print("geocoding chunk %r to %r" %(i-split,i))
    t=1
    while (t<=maxtries):
        response = requests_session.request(**kwargs)
        if (response.status_code == 200):
            res=pd.read_csv(StringIO.StringIO(response.content.decode('utf-8')),sep=",",quotechar='"')
            t=maxtries+1
        elif (response.status_code == 400):
            print("chunk %r to %r generated an exception:\n%r" %(i-split,i,response.content))
            res=df
            t=maxtries+1
        else:
            print("chunk %r to %r generated an exception, trying again:\n%r" %(i-split,i,response.content))
            t+=1
            
    return res




#version monothread
#for events_subset in f.iter_dataframes(chunksize=split):
#    i+=split
#    print("Enrichissement addok/BAN: {}...".format(i))
#    liste.append(adresse_submit(events_subset))
#    # Insert here applicative logic on each partial dataframe.
#    pass    

#multithread
with concurrent.futures.ThreadPoolExecutor(max_workers=nthreads) as executor:
    enrich={executor.submit(adresse_submit,subset) for subset in f.iter_dataframes(chunksize=split)}
    for s in concurrent.futures.as_completed(enrich):  
        j+=split
        try:
            liste.append(s.result())
        except Exception as exc:
            print("chunk %r to %r generated an exception: %r\n%r" %(j-split,j,exc,s))
        else:
            if ((j%verbosechunksize)==0:
                print("geocoded chunk %r to %r" %(j-split,j))


events=pd.concat(liste,ignore_index=True)

# Recipe outputs
out = d.Dataset("20161122_pve_securite_routiere_sample_geocoded")
out.write_with_schema(events)
