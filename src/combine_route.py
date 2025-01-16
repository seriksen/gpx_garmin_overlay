from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from .upload_route import get_uploaded_files
from .video_utils import extract_first_frame

def configure_combine_route(app):
    @app.route('/combine', methods=['GET', 'POST'])
    def combine():
        uploaded_files = get_uploaded_files(app.config['UPLOAD_FOLDER'])

        extract_first_frame(app.config['VIDEO_PATH'])

        return render_template('position_overlays.html',
                               frame='frame1.jpg',
                               height=app.config['VIDEO_HEIGHT'],
                               width=app.config['VIDEO_WIDTH'],
                               uploaded_files=uploaded_files)
