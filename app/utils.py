import librosa
from scipy import stats
import numpy as np

# Genre dictionary from colab environment
genre_dict = {0: 'metal', 1: 'classical', 2: 'pop', 3: 'country', 4: 'disco',
              5: 'reggae', 6: 'blues', 7: 'jazz', 8: 'rock', 9: 'hiphop'}

## Load the Song: First, we need a function to load the uploaded song and ensure it's at the required sample rate.

def load_song(song_path, sr= 22050):
  signal, _ = librosa.load(song_path, sr = sr)
  return signal

## Segment Extraction: From the loaded song, extract multiple 30-second segments.

def extract_segments(signal,  sr, segment_duration = 30, num_segments = 5):

  # Calculate the number of samples per segment
  num_samples_per_segment = int(len(signal) / num_segments)

  # Extract segments
  segments = [signal[i:i+num_samples_per_segment] for i in range(0, len(signal), num_samples_per_segment)][:num_segments]

  return segments

## Feature Extraction: Extracting the same features on which our models have been trained but from one 30 sec segment. This function returns the extracted data into the format which our model expects.

def extract_features(segment, sr, n_mfcc=13, n_fft=2048, hop_length=512):

    # MFCC
    mfcc = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
    mfcc = mfcc.T


    # Mel Spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=segment, sr=sr, n_fft=n_fft, hop_length=hop_length)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Spectral Contrast
    contrast = librosa.feature.spectral_contrast(y=segment, sr=sr, n_fft=n_fft, hop_length=hop_length)

    # Chroma feature
    chroma = librosa.feature.chroma_stft(y=segment, n_fft=n_fft, sr=sr, hop_length=hop_length)

    print("MFCC shape:", mfcc.shape)
    print("Mel Spectrogram shape:", mel_spectrogram.shape)
    print("Contrast shape:", contrast.shape)
    print("Chroma shape:", chroma.shape)
    
    # Transpose the Mel Spectrogram, Contrast, and Chroma features
    mel_spectrogram_transposed = np.transpose(mel_spectrogram, (1, 0))
    contrast_transposed = np.transpose(contrast, (1, 0))
    chroma_transposed = np.transpose(chroma, (1, 0))

    # Concatenate features into one numpy array
    features = np.concatenate([
        mfcc,
        mel_spectrogram_transposed,
        contrast_transposed,
        chroma_transposed
    ], axis=-1)

    return features

## A function to Preprocess the data 

def preprocess_song(song_path, sr=22050, segment_duration=30, num_segments=5, model_type='CNN'):
    # Load the song and extract segments
    signal = load_song(song_path, sr)
    segments = extract_segments(signal, sr, segment_duration, num_segments)

    # Preprocess each segment
    preprocessed_segments = [extract_features(segment, sr) for segment in segments]

    # Reshape for CNN if needed
    if model_type == 'CNN':
        preprocessed_segments = [np.expand_dims(segment, axis=-1) for segment in preprocessed_segments]

    return preprocessed_segments

## Predict on Segments: Predict the genre for each 30-second segment:

def predict_segments(model, segments, sr, model_type):
  predictions = []
  for segment in segments :
    features = extract_features(segment , sr)
    if model_type == 'CNN':
        # Reshape for CNN (add channel dimension)
        features = np.expand_dims(features, axis=-1)
    features = np.expand_dims(features, axis = 0)
    prediction = model.predict(features)
    predicted_label = np.argmax(prediction , axis = 1 )[0]
    predictions.append(predicted_label)
  return predictions

## Voting: Use the mode (most common value) from the segment predictions to decide the final genre:

def vote(predictions):
    if len(predictions) == 0:
        # Handle the case where there are no predictions
        print("No predictions")
        return None  # Or some default value or error handling
    else:
        mode_result = stats.mode(predictions)
        if isinstance(mode_result.mode, np.ndarray):
            if len(mode_result.mode) > 0:
                return mode_result.mode[0]
            else:
                # Handle the case where mode cannot be computed
                print("Mode cannot be computed")
                return None  # Or some default value or error handling
        else:
            # If mode_result.mode is a scalar
            return mode_result.mode

## Main Prediction Function: This function will combine all the above functions and give us a final prediction.

def predict_song(model, song_path , genre_dict, sr= 22050 , segment_duration = 30, num_segments= 5, model_type = 'CNN'):

  ## Load the song
  signal = load_song(song_path , sr)

  ## Extract segments
  segments = extract_segments(signal , sr , segment_duration, num_segments)

  ## Get predictions for each segment
  predictions = predict_segments(model, segments, sr, model_type)

  ## Vote to get the final prediction
  final_prediction_index = vote(predictions)
  print("Final Prediction Index:", final_prediction_index)
  final_prediction_genre = genre_dict.get(final_prediction_index, "Unknown")

  return final_prediction_genre



