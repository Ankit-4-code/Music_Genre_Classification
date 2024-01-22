'''
This .py file is used to test the librosa load function and preprocess_song function inside the docker container image.
I was facing a bug with librosa_load due to sound library dependicies and had to use conda virtual env conda-forge to finally solve it.

'''

import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

## Add the root directory to sys.path
if root_dir not in sys.path:
    sys.path.append(root_dir)
from app.utils import load_song, preprocess_song

SONG_PATH = "sampleSong\Dua Lipa - New Rules (Official Music Video) (320 kbps).mp3"
## Replace 'path_to_audio_file' with the actual path of an audio file in the container
signal = load_song(SONG_PATH)

## Check the output
print(signal)

## Preprocess the song
preprocessed_data = preprocess_song(SONG_PATH)

## If you want to see more details about each segment, you can loop through them
if preprocessed_data is not None:
    for i, segment in enumerate(preprocessed_data):
        print(f"Segment {i+1}: {segment.shape}")

## Check the output and print max values
if preprocessed_data is not None:
    for i, segment in enumerate(preprocessed_data):
        max_value = segment.max()
        print(f"Max value in segment {i+1}: {max_value}")
else:
    print("No preprocessed data available.")