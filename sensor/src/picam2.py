import datetime
import time
import os

from picamera2 import Picamera2
from picamera2.encoders import Quality

# create output folder
folder_name = "out"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
filename = f'{folder_name}/output_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4'

picam2 = Picamera2()
picam2.start_and_record_video(
    filename, duration=60*120, quality=Quality.VERY_HIGH)
