from utils import load_song, preprocess_song

SONG_PATH = "/app/Dua Lipa - New Rules (Official Music Video) (320 kbps).mp3"
# Replace 'path_to_audio_file' with the actual path of an audio file in the container
signal = load_song(SONG_PATH)

# Check the output
print(signal)

# Preprocess the song
preprocessed_data = preprocess_song(SONG_PATH)

# If you want to see more details about each segment, you can loop through them
if preprocessed_data is not None:
    for i, segment in enumerate(preprocessed_data):
        print(f"Segment {i+1}: {segment.shape}")

# Check the output and print max values
if preprocessed_data is not None:
    for i, segment in enumerate(preprocessed_data):
        max_value = segment.max()
        print(f"Max value in segment {i+1}: {max_value}")
else:
    print("No preprocessed data available.")