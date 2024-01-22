'''
This is the file which contains unit tests for all the functions in utils.py inside the app folder.

'''

import unittest
from unittest.mock import Mock, patch
import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

## Add the root directory to sys.path
if root_dir not in sys.path:
    sys.path.append(root_dir)
from app.utils import load_song, extract_segments, extract_features, preprocess_song, predict_song, predict_segments, vote, genre_dict

## Class to test librosa load function
class TestLoadSong(unittest.TestCase):
    def test_load_valid_song(self):
        ## Path to a valid test audio file
        valid_song_path = "D:\ML\Music Genre Classification\sampleSong\Eminem - My Name Is (Dirty Version) (Official Music Video) (320 kbps)(1).mp3"
        result = load_song(valid_song_path)
        self.assertIsNotNone(result)

    def test_load_invalid_song(self):
        ## Path to an invalid or non-existent audio file
        invalid_song_path = "path/to/invalid/audio.wav"
        result = load_song(invalid_song_path)
        self.assertIsNone(result)

## Class to test extract_segments function
class TestExtractSegments(unittest.TestCase):
    def test_extract_segments_normal(self):
        ## Mock a signal array (use a real example or a dummy numpy array)
        mock_signal = np.random.randn(22050 * 30)  # Assuming 30 seconds signal
        result = extract_segments(mock_signal, 22050, 30, 5)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(len(segment) == 22050 * 6 for segment in result))  # Each segment should be of equal length

    def test_extract_segments_short_audio(self):
        ## Mock a shorter signal array
        short_signal = np.random.randn(22050 * 10)  # 10 seconds signal
        result = extract_segments(short_signal, 22050, 30, 5)
        self.assertEqual(len(result), 0)  # Should return an empty list for short audio


## Class to test extract_features function
class TestExtractFeatures(unittest.TestCase):
    def test_extract_features(self):
        ## Mock a segment array (use a real example or a dummy numpy array)
        mock_segment = np.random.randn(22050 * 6)  # 6 seconds segment

        ## Sample rate
        sr = 22050

        ## Call the extract_features function
        features = extract_features(mock_segment, sr)

        ## Ensure the features are not None and have expected shape
        self.assertIsNotNone(features)
        self.assertEqual(features.shape[1], 160)  

## Class to test preprocess_song function
class TestPreprocessSong(unittest.TestCase):
    def test_preprocess_valid_song(self):
        ## Path to a valid test audio file
        valid_song_path = "D:\ML\Music Genre Classification\sampleSong\Eminem - My Name Is (Dirty Version) (Official Music Video) (320 kbps)(1).mp3"

        ## Call the preprocess_song function
        preprocessed_data = preprocess_song(valid_song_path, sr=22050, segment_duration=30, num_segments=5, model_type='CNN')

        ## Check if the preprocessed data is not None and has expected properties
        self.assertIsNotNone(preprocessed_data)
        self.assertTrue(all(segment.shape[0] == 259 for segment in preprocessed_data))  # Assuming 259 is the expected shape for your model

    def test_preprocess_invalid_song(self):
        ## Path to an invalid or non-existent audio file
        invalid_song_path = "path/to/invalid/audio.wav"

        ## Call the preprocess_song function
        preprocessed_data = preprocess_song(invalid_song_path, sr=22050, segment_duration=30, num_segments=5, model_type='CNN')

        ## Check if the preprocessed data is None
        self.assertIsNone(preprocessed_data)


## Class to test predict song function
class TestPredictSegments(unittest.TestCase):
    def setUp(self):
        self.mock_model = Mock()
        self.mock_model.predict.side_effect = lambda x: np.random.rand(x.shape[0], 10)

    @patch('app.utils.extract_features')
    def test_predict_segments(self, mock_extract):
        ## Mock extract_features to return dummy data of the correct shape
        mock_extract.return_value = np.random.rand(259, 160)

        ## Create mock segments
        mock_segments = [np.random.randn(259, 160, 1) for _ in range(5)]

        ## Call the predict_segments function
        predictions = predict_segments(self.mock_model, mock_segments, sr=22050, model_type='CNN')

        ## Assertions
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions), 5)

## Class to test vote function
class TestVoteFunction(unittest.TestCase):

    def test_vote_with_empty_predictions(self):
        predictions = []
        result = vote(predictions)
        self.assertIsNone(result, "Vote should return None for empty predictions")

    def test_vote_with_clear_mode(self):
        predictions = [1, 2, 2, 3, 2]
        result = vote(predictions)
        self.assertEqual(result, 2, "Vote should return the most common value")

    def test_vote_with_no_clear_mode(self):
        predictions = [1, 2, 3, 4, 5]
        result = vote(predictions)
        self.assertIn(result, predictions, "Vote should return one of the values when there is no clear mode")

## Class to test predict_song function 
class TestPredictSong(unittest.TestCase):

    def setUp(self):
        ## Create a mock model
        self.mock_model = Mock()
        self.mock_model.predict.return_value = np.random.rand(1, 10)

    @patch('app.utils.load_song')
    @patch('app.utils.extract_segments')
    @patch('app.utils.predict_segments')
    @patch('app.utils.vote')
    def test_predict_song_successful(self, mock_vote, mock_predict_segments, mock_extract_segments, mock_load_song):
        ## Setup mock return values
        mock_load_song.return_value = np.random.randn(22050 * 30)
        mock_extract_segments.return_value = [np.random.randn(259, 160) for _ in range(5)]
        mock_predict_segments.return_value = [1, 1, 2, 2, 2]  # Mocked predictions
        mock_vote.return_value = 2  # Mocked final vote

        ## Call predict_song
        result = predict_song(self.mock_model, 'path/to/song.mp3', genre_dict)

        ## Assertion
        self.assertEqual(result, genre_dict[2])

    @patch('app.utils.load_song')
    def test_predict_song_invalid_file(self, mock_load_song):
        ## Setup mock return value
        mock_load_song.return_value = None

        ## Call predict_song with an invalid file path
        result = predict_song(self.mock_model, 'path/to/invalid_song.mp3', genre_dict)

        ## Assertion
        self.assertEqual(result, "Unsupported file format or corrupt file.")

if __name__ == '__main__':
    unittest.main()


