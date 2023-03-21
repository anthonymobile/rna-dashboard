from flask import Flask, request, send_from_directory
from flask_frozen import Freezer

from Map import fullscreen_map

app = Flask(__name__)
# freezer = Freezer(app)

@app.route("/")
def homepage():
    return fullscreen_map(request.base_url).get_root().render()

# if __name__ == '__main__':
#     freezer.freeze()
