import re;
import json;
import requests;
from bs4 import BeautifulSoup;
from datetime import date;
from tabulate import tabulate

def get_forcast_data(): 
    """
        get the data world-weather from web
    """
    
    url = 'https://world-weather.info/'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "cookie": "celsius=1"
    }
    response = requests.get(url, headers=headers)
    
    if response.ok: 
        soup = BeautifulSoup(response.content, 'html.parser')
        resorts = soup.find('div', id='resorts')

        re_cities = r'">([\s\w]+)<\/a><span>'
        cities = re.findall(re_cities, str(resorts))
        
        re_temps = r'<span>(\+\d+|\-\d+)<span'
        temps = re.findall(re_temps, str(resorts))
        temps = [int(temp) for temp in temps]
        
        conditions_tags = resorts.find_all('span', attrs={'class': 'tooltip'})
        conditions = [condition.get('title') for condition in conditions_tags]
        
        data = zip(cities, temps, conditions)
        return data
    
    return False
    

def get_forcast_txt():
    """
        get the data world-weather from web and export data 
        to file txt 
    """
    
    data = get_forcast_data()
    
    if data:
        today = date.today().strftime('%d/%m/%Y')
        table = tabulate(data, headers=["City","Temp.", "Condition"], tablefmt='fancy_grid')
        with open('output.txt', 'w', encoding="utf-8") as f:
            f.write('Popular Cities Forcast' + '\n')
            f.write(today + '\n')
            f.write('=' * 24 + '\n')
            f.write(table)

def get_forcast_json():
    """
        get the data world-weather from web and export data 
        to file json 
    """
    
    data = get_forcast_data()
    
    if data:
        today = date.today().strftime('%d/%m/%Y')
        cities = [{"city": city, "temp": temp, "condition": condition} for city, temp, condition in data]
        data_json = { 
                     "title": "Popular Cities Forcast",
                     "date": today,
                     "cities": cities
                    }
        with open('output.json', 'w') as f:
            json.dump(data_json, f)
          
        
if __name__ == "__main__":
    get_forcast_txt()  
    get_forcast_json()