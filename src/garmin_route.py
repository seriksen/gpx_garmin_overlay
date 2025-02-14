from flask import render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from .upload_route import get_uploaded_files
from .upload_route import get_uploaded_files
from .garmin_utils import read_file, get_sport, get_recorder_information, get_activity_points, create_plots

def configure_garmin_route(app):
    @app.route('/garmin', methods=['GET', 'POST'], endpoint='garmin')
    def display_garmin():
        uploaded_files = get_uploaded_files(app.config['UPLOAD_FOLDER'], return_full_path=True)


        """
        This is where the FIT file information is handled.
        For this display, we only need the activity dictionary.
        If we like it, we will create videos for each bit based on where they are placed later.
        This screen also allows for cropping.
        """
        #activity_info = get_activity_points(uploaded_files)
        if app.config['FITNESS_PATH'] is None:
            files = [file for file in uploaded_files if file.endswith(('.fit', '.gpx'))]
            
            if len(files) == 0:
                fitness_path = None
                return render_template('upload.html')
            else:
                # Select the first video file
                # TODO: Create popup box to select video file
                fitness_path = files[0]

        else:
             fitness_path = app.config['FITNESS_PATH']

        if fitness_path:
             fitness_data = read_file(fitness_path)
             if fitness_data:
                 activity_info = get_activity_points(fitness_data)
                 if activity_info is not None:
                     plots = create_plots(activity_info)
                     sport = get_sport(fitness_data)
                     recorder =  get_recorder_information(activity_info)
                     return render_template('garmin.html', 
                                            activity_info=activity_info, 
                                            uploaded_files=uploaded_files,
                                            plots=plots,
                                            sport=sport,
                                            recorder=recorder)

        return render_template('garmin.html', activity_info=None, uploaded_files=uploaded_files)
    