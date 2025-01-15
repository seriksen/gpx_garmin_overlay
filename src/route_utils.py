from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

def configure_app_settings(app):
    UPLOAD_FOLDER = 'uploads'
    FRAME_FOLDER = 'frames'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['FRAME_FOLDER'] = FRAME_FOLDER
    app.config['VIDEO_PATH'] = None
    app.config['FITNESS_PATH'] = None
    app.config['VIDEO_LENGTH'] = None

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(FRAME_FOLDER, exist_ok=True)
