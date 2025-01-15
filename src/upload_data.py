import os
import cv2
from werkzeug.utils import secure_filename

def get_uploaded_files(UPLOAD_FOLDER):
    """Return a list of uploaded file names."""
    files = []
    if os.path.exists(UPLOAD_FOLDER):
        files = os.listdir(UPLOAD_FOLDER)
    return files

def save_video(file, UPLOAD_FOLDER):
    """Save the uploaded video file and return its path."""
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

def extract_first_frame(video_path):
    """Extract the first frame from a video file and save it as an image."""
    video_capture = cv2.VideoCapture(video_path)
    success, frame = video_capture.read()
    
    if success:
        frame_path = os.path.join(FRAME_FOLDER, 'frame1.jpg')
        cv2.imwrite(frame_path, frame)  # Save the first frame as an image
        video_capture.release()
        return 'frame1.jpg'
    else:
        video_capture.release()
        return None
