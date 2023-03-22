from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

app.config['FREEZER_BASE_URL'] = "http://localhost:5000"
app.config['FREEZER_DESTINATION'] = "../../site_staging"

if __name__ == '__main__':
    freezer.freeze()