import sys
import os
import numpy as np
import bentoml
from bentoml.io import JSON


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

## Add the root directory to sys.path
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.utils import vote, genre_dict



runner = bentoml.keras.get("cnn_keras_model:latest").to_runner()

svc = bentoml.Service("cnn_keras_model_service", runners=[runner])

@svc.api(input= JSON(), output=JSON())
async def classify_genre(request_json):

    features_list = request_json["features"]

    ## Check if the features need conversion from JSON lists to NumPy arrays
    if not isinstance(features_list[0], np.ndarray):
        features = [np.array(segment) for segment in features_list]
    else:
        features = features_list
    ## Reshape data and run predictions
    predictions = []
    for segment in features:
        segment = np.expand_dims(segment, axis=0)  # Add batch dimension
        # Directly use runner for prediction on preprocessed features
        prediction = await runner.async_run(segment)
        predictions.append(np.argmax(prediction, axis=1)[0])

    ## Aggregate predictions
    final_prediction_index = vote(predictions)
    predicted_genre = genre_dict.get(final_prediction_index, "Unknown")

    return {"genre": predicted_genre}



