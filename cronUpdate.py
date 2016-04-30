from models.GeoNewsUpdater import *
import time

while True:
    gnu = GeoNewsUpdater()
    _gnu = gnu.getGeoNews()
    print ('ticked')
    time.sleep(300)
