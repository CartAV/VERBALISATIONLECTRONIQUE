# -*- coding: utf-8 -*-
import dataiku as d
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

step=1000

def adresse_submit(file):
    requests_session = requests.Session()
    print("Enrichissement addok/BAN: {}...".format(file))
    kwargs = {
        'data': OrderedDict([
            ('columns', 'v1'), 
            ('columns', 'adr'),
            ('citycode', 'code_insee')
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
events = f.get_dataframe()

#splitting
for k in range(step,len(events)+step,step):
    file="tmp_{}".format(k)
    events[k-step:k].to_csv(file,sep=";",quotechar='"',index=false)
    

# Recipe outputs
out = d.Dataset("20161122_pve_securite_routiere_sample_geocoded")
out.write_with_schema(events)
