from models.applespider import AppleSpider
from models.contentparser import ContentParser
import json
from models.gmap import Gmap
import time
import sqlite3

class GeoNewsUpdater:
    dbName = 'assets/GeoNews.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS geonews ( url text, location text, title text, updateTime integer )''')

    def __del__(self):
        self.conn.close()

    def uniqify(self, seq, idfun=None): 
       # order preserving
       if idfun is None:
           def idfun(x): return x
       seen = {}
       result = []
       for item in seq:
           marker = idfun(item)
           # in old Python versions:
           # if seen.has_key(marker)
           # but in new ones:
           if marker in seen: continue
           seen[marker] = 1
           result.append(item)
       return result

    def retrieveNews (self, url ):
        self.cursor.execute('SELECT location, updateTime FROM geonews WHERE url = ?', (url,))
        locations = self.cursor.fetchall()
        return locations
    
    # return locations
    def addNews ( self, url, lastUpdateTime, locations, title ):
        for location in locations:
            self.cursor.execute('INSERT INTO geonews VALUES (?, ?, ?, ?)', (url, location, title, lastUpdateTime))
            self.conn.commit()
        return locations

    def getGeoNews(self):
        appleSpider = AppleSpider()
        cp = ContentParser("assets/location.dict")
        gmap = Gmap()
        geoNews = []

        def callback( title, content, url, lastUpdateTime ):
            print (title)
            timestamp = int ( time.mktime( time.strptime ( lastUpdateTime, "%Y-%m-%d %H:%M:%S %Z" ) ) )
            locations = self.retrieveNews (url)
            cp.setContent(content)
            locations = [location for (location,updateTime) in self.retrieveNews ( url )] or self.addNews( url, lastUpdateTime, self.uniqify(cp.getLocations()), title )
            
            geocode = ''
            for location in locations:
                geocode = json.loads( gmap.getGeoLocation(location) )
                if location != '香港':
                    geoNews.append([ url, location, geocode.get('geometry'), lastUpdateTime ])

        appleSpider.setCallback(callback)
        appleSpider.crawl(1)
        return (geoNews)
