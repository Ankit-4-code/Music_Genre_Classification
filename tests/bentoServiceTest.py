import sys
import os
import requests
import numpy as np
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

## Add the root directory to sys.path
if root_dir not in sys.path:
    sys.path.append(root_dir)
from app.utils import preprocess_song

## Replace with the path to your test song
song_path = "D:\ML\Music Genre Classification\sampleSong\Eminem - The Real Slim Shady (Official Video - Dirty Version) (320 kbps).mp3"

## Use your preprocessing function
preprocessed_data = preprocess_song(song_path)
serialized_data = [segment.tolist() for segment in preprocessed_data]

""" for segment in preprocessed_data:
    print(segment.shape)
 """

response = requests.post(
    "http://127.0.0.1:3000/classify_genre", 
    json={"features": serialized_data},
    headers={"content-type": "application/json"}
)

print(response.json())