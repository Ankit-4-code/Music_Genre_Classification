from app.model import build_and_load_model
from app.utils import predict_song, genre_dict

## Path to saved model
MODEL_PATH = 'model_CNN.h5'
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