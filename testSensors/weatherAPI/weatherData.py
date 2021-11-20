import myData
import requests
import json

api_key     = myData.api_key
city        = myData.city
city_name   = myData.city_name
state       = myData.state
country     = myData.country

""" Set City """
def set_city(city):
    # base_url    = 'api.openweathermap.org/data/2.5/weather?q='
    # complete_url = base_url + city_name + ',' + state + ',' + country + '&appid=' + api_key

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
 
    response = requests.get(complete_url)
 
    x = response.json() 
 
    if x["cod"] != "404": 
        # text_to_speech("your city is set")
        valid = True
    else:
        # text_to_speech("Invalid city name, give another one.")
        valid = False
 
    return valid

def weather(city_name):
 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json() 
 
    if x["cod"] != "404": 
     
        y = x["main"] 
        tempK = y["temp"]
        tempC = round( tempK - 273.15, 1 )
        tempF = round( (9/5) * tempC + 32, 1 )
        # current_temperature = y["temp"]
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"]
        z = x["weather"] 
    
        weather_description = z[0]["description"] 
     
        # print following values 
        print(f'Temperature             = {tempK}K / {tempC}C / {tempF}F\n')
        print(f'Atmospheric Pressure    = {current_pressure}hPa\n')
        print(f'Humidity                = {current_humidiy}%\n')
        print(f'Description             = {weather_description}\n')
 
    else: 
        print("City Not Found ") 
 
    # return current_temperature, weather_description
    return tempK, tempC, tempF, weather_description
