import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

## Add the root directory to sys.path
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.model import build_and_load_model
from app.utils import predict_song, genre_dict

## Path to saved model
WEIGHTS_PATH = 'models\model_weights.keras'
## Path to a sample song file
SONG_PATH = "sampleSong\pop.00010.wav"

def main():
    ## Load the model
    model = build_and_load_model(WEIGHTS_PATH)

    print(model.summary())
    
    ## Predict the genre of the song
    genre_prediction = predict_song(model, SONG_PATH, genre_dict, model_type= 'CNN')
    
    print(f"The predicted genre is: {genre_prediction}")

if __name__ == "__main__":
    main()