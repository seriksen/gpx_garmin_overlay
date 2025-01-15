"""
Functions to be implemented:
- create_videos:
- display_parameters:
"""

from garmin_fit_sdk import Decoder, Stream
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import awkward as ak
import plotly.express as px
import plotly.graph_objs as go
import plotly
import json

def read_file(file_path: str) -> dict | None:
    
    stream = Stream.from_file(file_path)
    decoder = Decoder(stream)
    messages, errors = decoder.read(
            apply_scale_and_offset = True,
            convert_datetimes_to_dates = True,
            convert_types_to_strings = True,
            enable_crc_check = True,
            expand_sub_fields = True,
            expand_components = True,
            merge_heart_rates = True,
            mesg_listener = None)

    if len(errors) > 0:
        print(f"Errors reading file: {errors}")
        return None
    else:
        return messages
    
def get_sport(messages: dict) -> str | None:
    if 'sport_mesgs' in messages:
        # If more than one sport; ie triathalon, this won't work yet
        record = messages['sport_mesgs'][0]
        if 'sport' in record:
            return record['sport']
        else:
            return None
    else:
        return None

def get_recorder_information(messages: dict) -> str | None:
    if 'file_id_mesgs' in messages:
        record = messages['device_info_megs'][0]['garmin_product']
        return record
    else:
        return None

def get_activity_points(messages: dict) -> pd.DataFrame | None:
    if 'record_mesgs' in messages:
        # Create a pandas DataFrame from the record_mesgs
        # This DataFrame will contain columns for time, distance, speed, and heart rate
        df = pd.DataFrame(messages['record_megs'])
        df['speed_kmph'] = df['enhanced_speed'] * 3.6  # Convert speed from m/s to km/h
        df['speed_mph'] = df['speed_kmph'] * 0.621371  # Convert speed from km/h to mph
        df['distance_km'] = df['distance'] / 1000  # Convert distance from meters to kilometers
        df['distance_miles'] = df['distance_km'] * 0.621371  # Convert distance from km to miles
        return df
    else:
        return None

def create_speed_plot(df: pd.DataFrame) -> json:

    fig = px.line(df, x='timestamp', y='speed_kmph', title='Speed (km/h)')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_map_plot(df: pd.DataFrame) -> json:
    fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='speed_kmph',
                          title='Location and Speed (km/h)', hover_name='timestamp')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)