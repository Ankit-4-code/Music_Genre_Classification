from app import app
from flask import request, render_template
from werkzeug.utils import secure_filename
import os
from .model import build_and_load_model
from .utils import predict_song, genre_dict

app.config['UPLOAD_FOLDER'] = 'uploads'

# Load the model (only once, e.g., when starting your server)- Global
model_type = 'CNN'  # Change to 'LSTM' or 'CNN' based on the model
WEIGHTS_PATH = 'D:\ML\Music Genre Classification\model_weights.keras'

model = build_and_load_model(WEIGHTS_PATH)

@app.route('/')
@app.route('/index')
def index():
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file is received
    if 'file' not in request.files:
        return "No file uploaded.", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected.", 400

    # Save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)


    # Make a prediction
    genre_prediction = predict_song(model, filepath, genre_dict, model_type= 'CNN')

    # After prediction, delete the file to save memory
    os.remove(filepath)

    # Return the result (you can also render a result page)
    return (f"The predicted genre is: {genre_prediction}<br><br>"
            f"<a href='/'>Upload another song</a>")
