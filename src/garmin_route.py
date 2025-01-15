from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from .upload_route import get_uploaded_files

def configure_garmin_route(app):
    @app.route('/garmin', methods=['GET', 'POST'])
    def garmin():
        uploaded_files = get_uploaded_files(app.config['UPLOAD_FOLDER'])
        return render_template('garmin.html', uploaded_files=uploaded_files)
