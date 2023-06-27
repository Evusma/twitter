import pandas as pd
import geopandas as gpd
import requests
from datetime import date, timedelta

def earthquake_updates():
    d_1 = str(date.today() - timedelta(days=1))
    d_2 = str(date.today() - timedelta(days=2))
    
    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={d_2}&endtime={d_1}'
    
    reponse = requests.get(url)
    
    if reponse.status_code != 200: return "Oops, there is a problem with the url! No updates today :("
    
    try:
        gdf = gpd.read_file(url)
        gdf = gdf.sort_values('mag', ascending=False)
        pd.set_option('display.max_columns', None)
        gdf.reset_index(inplace=True)
        col = [2, 3, 4, 12, 14, 28]
        data = gdf[gdf.columns[col]]
                        
        number = str(len(data))
        mag = str(data.loc[0, 'mag'])
        place = data.loc[0, 'place']
        if place is None:
            place = "unknown"
        time = str(pd.to_datetime(gdf.loc[0, 'time'], utc=True, unit='ms'))   
        alert = data.loc[0, 'alert']
        if alert is None:
            alert = "With no alert level"
        else:
            alert = f'With {alert} alert level'
        
        tsunami = int(data.loc[0, 'tsunami'])
        if tsunami == 0:
            tsunami = "no risk of tsunami"
        else:
            tsunami = "risk of tsunami"
        depth = data.loc[0, 'geometry'].z
        tweet = f'{time[:10]}: there were {number} earthquakes in the world. The largest registered magnitude was {mag} with a depth of {depth} Km. Location: {place}. Time: {time[11:19]} (UTC). {alert} and {tsunami}. \n - Data from USGS'
        return tweet
    except:
        return "Oops, there is a problem with the document, I can't read it! No updates today :("
    
    
def main():
    a = earthquake_updates()
    print(a)
    
    
if __name__ == "__main__":
    main()
