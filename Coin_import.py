import requests
import pandas as pd
import json, os, datetime, time


# api-endpoint
URL = "https://api.coinmarketcap.com/v1/ticker/"
 
# location given here
limit = "0"#(int) limit - return a maximum of [limit] results (default is 100, use 0 to return all results)
 
# defining a params dict for the parameters to be sent to the API
PARAMS = {'limit':limit}
def collect():
    # api-endpoint
    URL = "https://api.coinmarketcap.com/v1/ticker/"
 
    # location given here
    limit = "0"#(int) limit - return a maximum of [limit] results (default is 100, use 0 to return all results)
 
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'limit':limit}
    
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
     
    # extracting data in json format
    data = r.json()
    
    RAW = pd.DataFrame(columns=[k for k in data[0]])
    # add to RAW
    RAW = RAW.append([pd.Series([catch(i) for k,i in i.items()],index=[k for k in data[0]]) for i in data])
    RAW['last_updated'] = pd.to_datetime(RAW['last_updated'],unit='s')
    
    # if file does not exist write header 
    file = "RAW_"+str(datetime.date.today())+"_h"+str(datetime.datetime.now().hour)+".csv"
    if not os.path.isfile(file):
        try:
            Temp = pd.DataFrame.read_csv("RAW_"+str(datetime.date.today()-datetime.timedelta(hours=1))+".csv")
            
        except Exception as e:
            print("No previous file")
        RAW.to_csv(file,header ='column_names')
    else: # else it exists so append without writing the header
        RAW.to_csv(file,mode = 'a',header=False)

def catch(i):
    try:
        return int(i)
    except Exception as e:
        try:
            return float(i)
        except Exception as e:
            return i

while True:
    try:
        collect()
    except Exception as e:
        print("Lost Connection trying again in 60 sek")
    time.sleep(60)

