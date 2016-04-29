# encoding=utf-8
import requests
import googlemaps
import json
import sqlite3
import time
import os

class Gmap:
    gmaps = googlemaps.Client(key='AIzaSyDDBrhr-8SGKa6t_O7IUmLzSTqOj89gQwE')
    dbName = 'assets/GeoNews.db'
    dictName = 'assets/location.dict'

    def __init__(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS locations ( name text, gmap_json text, partial_match boolean )''')

    # Build the sqlite db based on the dictionary to minimize location checking
    def build(self, dictionaryName=None):
        self.dictName = dictionaryName or self.dictName
        with open ( self.dictName ) as f:
            for line in f:
                place = line.split()[0]
                self.getGeoLocation ( place )


    # return the googlemap json location by inputting geo place name
    # new place will store into the sqlite db for performance enhancement
    def getGeoLocation(self, place):
        if place == '香港':
            return "{}"
        self.cursor.execute('SELECT gmap_json FROM locations WHERE name = ?', (place,))
        gmap_json = self.cursor.fetchone()

        if gmap_json is None:
            # Geocoding an address
            geocode = self.gmaps.geocode( '香港'+place )
            #print (type(geocode[0]))
            gmap_json = json.dumps ( geocode[0] )
            self.cursor.execute('INSERT INTO locations VALUES (?, ?, ?)', (place,gmap_json,geocode[0].get('partial_match'),))
            self.conn.commit()
            time.sleep(2) # sleep for two seconds to ensure next call is okay
        else:
            gmap_json = gmap_json[0]

        return gmap_json 

    def locate(self, place):
        geocode = self.gmaps.geocode( '香港'+place )
        if geocode[0].get('partial_match') == True:
            print ("Partial Match")

    def __del__(self):
        self.conn.close()

#gmap = Gmap()
#gmap.build()
#print(gmap.getGeoLocation('青衣長青邨青楊樓'))
#gmap.locate('新渡')
