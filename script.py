from PIL import Image as img
from urllib.request import Request, urlopen
import requests
import json
import twitter
from geopy.geocoders import Nominatim
import time
from datetime import datetime
from config import config



while(True):
    if(datetime.utcnow().hour in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23] and datetime.utcnow().minute == 0 and datetime.utcnow().second == 0):
        """ get the coords"""
        response = requests.get('http://api.open-notify.org/iss-now.json')
        resJson = json.loads(response.content.decode('utf-8'))
        lat = resJson['iss_position']['latitude']
        lon = resJson['iss_position']['longitude']

        geolocator = Nominatim()
        location = geolocator.reverse("{latitude}, {longitude}".format(latitude=lat, longitude=lon))
        try:
            message = location.raw['address']['country']
        except Exception as e:
            message = "Sea"

        """ save image """
        req = Request("https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/static/pin-s-airport+ff8000({longitude},{latitude})/{longitude},{latitude},0,0/1000x1000@2x?access_token={api_token}&attribution=false&logo=false".format(longitude=lon, latitude=lat, api_token=config['api_token']), headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        f = open('./ImageISS.jpg', 'wb')
        f.write(webpage)
        f.close()

        """ post on twitter """
        fichier=open('./ImageISS.jpg', 'rb')
        api = twitter.Api(consumer_key=config['consumer_key'],consumer_secret=config['consumer_secret'],access_token_key=config['access_token_key'],access_token_secret=config['access_token_secret'])
        api.UpdateProfile(location="lat: {} | lon: {}".format(lat, lon), description="Hi, my name is Neil. I've been created to celebrate the 50th anniversary of the moon landing the 21th of July 2019.\nHere is my creator: @MrAnyx")

        hour = "%02d" % datetime.utcnow().hour
        minute = "%02d" % datetime.utcnow().minute
        second = "%02d" % datetime.utcnow().second


        status = api.PostUpdate("It's {hour}:{minute}:{second} and the International Space Station is actually here: lat: {latitude}, lon: {longitude}.\nIt's 400 Km above : {message}".format(hour=hour, minute=minute, second=second, latitude=lat, longitude=lon, message=message), media=fichier)
        fichier.close()

        print("[INFO] La position de l'ISS a été postée à {hour}:{minute}:{second}".format(hour=hour, minute=minute, second=second))

        time.sleep(10)
