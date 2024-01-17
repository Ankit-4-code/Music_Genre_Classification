from app import app
from flask import request, render_template
from werkzeug.utils import secure_filename
import os
import requests
from .utils import preprocess_song
import logging

# configuration for logging
logging.basicConfig(level=logging.INFO)

app.config['UPLOAD_FOLDER'] = 'uploads'
BENTOML_URL = 'http://bento-service:3000/classify_genre'

## Load the model- Global
model_type = 'CNN'  ## Change to 'LSTM' or 'CNN' based on the model


@app.route('/')
@app.route('/index')
def index():
    return render_template('upload.html')

def allowed_file(filename):
    ## Check for allowed file extensions
    allowed_extensions = {'wav', 'mp3', 'flac', 'aac'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/predict', methods=['POST'])
def predict():
    ## Check if a file is received
    if 'file' not in request.files:
        logging.error("No file part in the request")
        return render_template('error.html', message="No file uploaded.")
    

    file = request.files['file']

    if file.filename == '':
        logging.error("No selected file")
        return render_template('error.html', message="No file selected.")
    ## Check if the file is of allowed type
    if not allowed_file(file.filename):
        logging.error("File format not supported")
        return render_template('error.html', message="Uploaded file is not a supported audio format. Please upload a valid audio file.")
    
    ## Store the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    logging.info(f"File saved at {filepath}")

    ## Preprocess the song
    preprocessed_data = preprocess_song(filepath)

    if preprocessed_data is None:  ## Checking if the song could not be loaded
        logging.error("Song could not be loaded or processed")
        os.remove(filepath)
        return render_template('error.html', message="Unsupported file format or corrupt file.")

    if not preprocessed_data:  ## Checking if no segments were extracted
        os.remove(filepath)
        return render_template('error.html', message="Audio file too short for analysis.")

    
    serialized_data = [segment.tolist() for segment in preprocessed_data]

    try : 
        ## Make a prediction
        response = requests.post(
            BENTOML_URL, 
            json={"features": serialized_data},
            headers={"content-type": "application/json"}
        )
        logging.info(f"Response from BentoML: {response.status_code}, {response.json()}")
    except Exception as e:
        logging.error(f"Error in making request to BentoML: {e}")
        os.remove(filepath)
        return render_template('error.html', message="Error in prediction.")

    #print("Raw Response from BentoML:", response.text)
    #print("Response from BentoML:", response.status_code, response.json())

    ## After prediction, delete the file to save memory
    os.remove(filepath)

    if response.status_code != 200:
        return render_template('error.html', message="Error in prediction.")

    genre_prediction = response.json().get("genre", "Unable to make a prediction.")

    return render_template('result.html', genre_prediction=genre_prediction)




