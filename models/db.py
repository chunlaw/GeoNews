import sqlite3
import datetime
import time
import json
from models.gmap import Gmap

class GeoNewsDb:

    def __init__(self):
        self.conn = sqlite3.connect('assets/GeoNews.db')
        self.cursor = self.conn.cursor()

    def getNews(self, recentMinutes=360):
        geoNews = []
        gmap = Gmap()
        timestamp = int(time.mktime(time.localtime())) - 60*recentMinutes
        print ( timestamp )
        self.cursor.execute('SELECT url, title, location, updateTime FROM geonews WHERE updateTime >= ? ORDER BY updateTime DESC', (timestamp,))
        news = self.cursor.fetchall()
        for (url, title, location, updateTime) in news:
            updateTime = datetime.datetime.fromtimestamp(updateTime).strftime("%Y-%m-%d %H:%M:%S") + " HKT"
            geocode = json.loads( gmap.getGeoLocation(location) )
            if location != '香港':
                geoNews.append([ url, title, location, geocode.get('geometry'), updateTime ])
        return geoNews

    def __del__(self):
        self.conn.close()
