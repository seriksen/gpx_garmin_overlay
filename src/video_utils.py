"""
Functions to be implemented:
- save_video(file: str) -> str:
- crop_video(video_path: str, start_time: float, end_time: float) -> str:
"""

import cv2
import os
from typing import Any

def extract_first_frame(video_path: str) -> str | None:
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

def get_video_information(video_path: str) -> dict[str, Any]:
    """Return video metadata such as duration, resolution, etc."""
    info_dict: dict[str, Any] = {}

    video_capture = cv2.VideoCapture(video_path)
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    
    info_dict['duration'] = duration
    info_dict['resolution'] = f'{int(width)}x{int(height)}'
    info_dict['fps'] = fps
    info_dict['frame_count'] = frame_count
    info_dict['codec'] = video_capture.get(cv2.CAP_PROP_FOURCC)
    info_dict['bitrate'] = video_capture.get(cv2.CAP_PROP_BITRATE)
    info_dict['file_size'] = os.path.getsize(video_path)

    video_capture.release()
    return info_dict
    

def format_file_size(size_in_bytes: int) -> str:
    """Format file size to KB, MB, or GB."""
    kb = size_in_bytes / 1024
    if 1 <= kb < 100:
        return f"{kb:.2f} KB"
    mb = kb / 1024
    if 1 <= mb < 100:
        return f"{mb:.2f} MB"
    gb = mb / 1024
    return f"{gb:.2f} GB"
    
def save_video(file: str) -> str | None:
    """Return the duration of the video in seconds."""
    video_capture = cv2.VideoCapture(video_path)
    duration = video_capture.get(cv2.CAP_PROP_DURATION)
    video_capture.release()
    return duration
