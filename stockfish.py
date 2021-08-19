import requests
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

range_ = [x for x in range(0,2000000,2000)]

district_hospital = []

for x in range_:
    try:
        offset = f'https://gis-dm.ndma.gov.in/server/rest/services/Oxy/district_hospital_details/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=objectid%20ASC&outSR=102100&resultOffset={x}&resultRecordCount=2000'
        data = requests.get(offset,verify=False)
        df = pd.json_normalize(data.json()['features'])
        district_hospital.append(df)
        if len(data.json()['features'])==0:
            break
        else:
            pass
    except:
        pass
        
main = pd.concat(district_hospital)
main = main.drop_duplicates()
main['attributes.created_date'] = [item[:-3] for item in main['attributes.created_date'].astype(str)]
main['attributes.last_edited_date'] = [item[:-3] for item in main['attributes.last_edited_date'].astype(str)]
main['attributes.created_date'] = [datetime.utcfromtimestamp(item).strftime('%Y-%m-%d %H:%M:%S') for item in main['attributes.created_date'].astype(int)]
main['attributes.last_edited_date'] = [datetime.utcfromtimestamp(item).strftime('%Y-%m-%d %H:%M:%S') for item in main['attributes.last_edited_date'].astype(int)]
main['attributes.district'].nunique()
main['attributes.hospital_name'].nunique()
main.to_csv('archive/' + 'abstract.csv',index=False)
