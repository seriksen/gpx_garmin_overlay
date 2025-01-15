from flask import Flask, render_template
from src.route_utils import configure_app_settings
from src.upload_route import configure_upload_route
from src.video_route import configure_video_route
from src.garmin_route import configure_garmin_route
import os

app = Flask(__name__)

# Configure directories
configure_app_settings(app)

# Upload route
configure_upload_route(app)

# Video route
configure_video_route(app)

# Garmin route
configure_garmin_route(app)

@app.route('/')
def welcome():
    uploaded_files = get_uploaded_files()
    return render_template('welcome.html', uploaded_files=uploaded_files)

@app.route('/combine')
def combine():
    uploaded_files = get_uploaded_files()
    return render_template('combine.html', uploaded_files=uploaded_files)

def get_uploaded_files():
    upload_folder = 'uploads'  # Make sure this matches your UPLOAD_FOLDER configuration
    files = []
    if os.path.exists(upload_folder):
        files = os.listdir(upload_folder)
    return files

if __name__ == '__main__':
    app.run(debug=True)