from flask import render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from .upload_route import get_uploaded_files
from .video_utils import get_video_information
import subprocess

def configure_video_route(app):

    @app.route('/video', methods=['GET', 'POST'], endpoint='video')
    def display_video():
        uploaded_files = get_uploaded_files(app.config['UPLOAD_FOLDER'], return_full_path=True)

        if app.config['VIDEO_PATH'] is None:
            # Select a video file from the uploaded files

            files = [file for file in uploaded_files if file.endswith(('.mp4', '.mov'))]
            
            if len(files) == 0:
                video_path = None
                return render_template('upload.html')
            else:
                # Select the first video file
                # TODO: Create popup box to select video file
                video_path = files[0]  

        else:
            video_path = app.config['VIDEO_PATH']

        if video_path:
            video_info = get_video_information(video_path)
            video_duration=video_info['duration']
        else:
            video_duration = 0

        return render_template('video.html', uploaded_files=uploaded_files, 
                               video_path=video_path, video_info=video_info,
                               video_duration=video_duration)

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    

    @app.route('/crop-video', methods=['POST'])
    def crop_video():
        data = request.json
        start_time = data['startTime']
        end_time = data['endTime']

        video_path = app.config['VIDEO_PATH']

        output_path = video_path.rsplit('.', 1)[0] + '_cropped.mp4'

        app.config['VIDEO_LENGTH'] = end_time - start_time

        try:
            subprocess.run([
                'ffmpeg',
                '-i', video_path,
                '-ss', str(start_time),
                '-to', str(end_time),
                '-c', 'copy',
                output_path
            ], check=True)
            return jsonify({'success': True, 'message': 'Video cropped successfully'})
        except subprocess.CalledProcessError:
            return jsonify({'success': False, 'message': 'Failed to crop video'}), 50