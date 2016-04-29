from models.applespider import AppleSpider
from models.contentparser import ContentParser
import json
from models.gmap import Gmap

def uniqify(seq, idfun=None): 
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

def getGeoNews():
    appleSpider = AppleSpider()
    cp = ContentParser("assets/location.dict")
    gmap = Gmap()
    geoNews = []

    def callback( content, url ):
        cp.setContent(content)
        geocode = ''
        for location in uniqify(cp.getLocations()):
            geocode = json.loads( gmap.getGeoLocation(location) )
            if location != '香港':
                geoNews.append([ url, location, geocode.get('geometry') ])

    appleSpider.setCallback(callback)
    appleSpider.crawl(1)
    return (geoNews)
