from flask import Flask
from models.GeoNewsUpdater import *
import json
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route("/")
def index():
    gnu = getGeoNews()
    return json.dumps(gnu,ensure_ascii=False).encode('utf8')

if __name__ == "__main__":
    app.run()
