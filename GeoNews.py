from flask import Flask
from models.db import *
import json
import sys

sys.stdout = sys.stderr

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route("/")
def index():
    gnu = GeoNewsDb()
    _gnu = gnu.getNews()
    return json.dumps(_gnu,ensure_ascii=False).encode('utf8')

if __name__ == "__main__":
    app.run()
