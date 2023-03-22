from flask import Flask, request
from Map import fullscreen_map

app = Flask(__name__,
            static_folder="assets",
            static_url_path="/assets"
            )

@app.route("/")
def homepage():
    return fullscreen_map(request.base_url).get_root().render()
