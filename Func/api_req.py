import requests

appid = 'secret'

def apiWeath_get(name):
    return requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={appid}').status_code

def apiWeather_find(post_id):
    url = f'https://api.openweathermap.org/data/2.5/find?q={post_id}&cnt=3&appid={appid}'
    res = requests.get(url).json()['list']
    return res