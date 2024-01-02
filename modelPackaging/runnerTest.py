import sys
import os
import numpy as np
import bentoml

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the root directory to sys.path
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.utils import preprocess_song, vote, genre_dict

def test_runner_with_song(song_path, model_name="cnn_keras_model:latest"):
    # Load and preprocess the song
    preprocessed_data = preprocess_song(song_path)

    # Load the runner
    runner = bentoml.keras.get(model_name).to_runner()

    runner.init_local()

    # Make predictions for each segment
    predictions = []
    for segment in preprocessed_data:
        # Ensure segment has correct shape for the model
        segment = np.expand_dims(segment, axis=0)  # Add batch dimension
        prediction = runner.run(segment)
        predictions.append(np.argmax(prediction, axis=1)[0])

    # Aggregate predictions to get final genre
    final_prediction_index = vote(predictions)
    predicted_genre = genre_dict.get(final_prediction_index, "Unknown")

    return predicted_genre

if __name__ == "__main__":
    # Replace with the path to your test song
    song_path = "D:\ML\Music Genre Classification\sampleSong\jazz.00025.wav"
    genre = test_runner_with_song(song_path)
    print(f"Predicted genre: {genre}")


