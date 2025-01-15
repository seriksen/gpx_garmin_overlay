from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

def configure_upload_route(app):

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():

        uploaded_files = get_uploaded_files(app.config['UPLOAD_FOLDER'])

        if request.method == 'POST':
            if 'video' not in request.files or 'fitness_data' not in request.files:
                return redirect(request.url)
            
            video_file = request.files['video']
            fitness_file = request.files['fitness_data']

            if video_file.filename == '' or fitness_file.filename == '':
                return redirect(request.url)

            if video_file and fitness_file:

                video_filename = secure_filename(video_file.filename)
                fitness_filename = secure_filename(fitness_file.filename)
                
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
                fitness_path = os.path.join(app.config['UPLOAD_FOLDER'], fitness_filename)

                app.config['VIDEO_PATH'] = video_path
                app.config['FITNESS_PATH'] = fitness_path
                
                video_file.save(video_path)
                fitness_file.save(fitness_path)

                uploaded_files = get_uploaded_files(app.config['UPLOAD_FOLDER'])    
                return render_template('upload.html', uploaded_files=uploaded_files)

        return render_template('upload.html', uploaded_files=uploaded_files)
    
def get_uploaded_files(UPLOAD_FOLDER, return_full_path=False):
    """Return a list of uploaded file names."""
    files = []
    if os.path.exists(UPLOAD_FOLDER):
        files = os.listdir(UPLOAD_FOLDER)
    if return_full_path:
        files = [os.path.join(UPLOAD_FOLDER, file) for file in files]  # Add full path if required
    return files
