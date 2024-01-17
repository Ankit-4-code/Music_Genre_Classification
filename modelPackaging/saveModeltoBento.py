import bentoml
import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

## Add the root directory to sys.path
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.model import build_and_load_model



WEIGHTS_PATH = '/app/models/model_weights.keras'

def load_model_and_save_to_bento(WEIGHTS_PATH):

    ## Load the model
    model =  build_and_load_model(WEIGHTS_PATH)

    ## save the model to local bento store
    bento_model = bentoml.keras.save_model("cnn_keras_model", model)
    print(f"Bento model Tag:{bento_model.tag}")




if __name__ == "__main__":
    load_model_and_save_to_bento(WEIGHTS_PATH)
