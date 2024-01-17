# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip
# Install audio libraries
#RUN apt-get update && apt-get install -y libsndfile1 libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg

RUN pip install -r requirements.txt
RUN pip install https://files.pythonhosted.org/packages/3f/b2/33372601ed71fb41049642f8f6e1e142215e8b5c3463df434fc8885db278/tensorflow-2.12.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Install supervisord && apt-get install -y supervisor
RUN apt-get update 


# Force refresh the cache from this point
# Change the comment to invalidate cache (e.g., # Force refresh 2024-01-12)


# Copy the necessary directories and files into the container
COPY models/ /app/models/
COPY modelPackaging/ /app/modelPackaging/
COPY app/ /app/app/

# Setup supervisord
#COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make port 3000 available to the world outside this container
EXPOSE 3000
#EXPOSE 5000
# Change to modelPackaging directory
WORKDIR /app/modelPackaging


# Save the model using BentoML
RUN python saveModeltoBento.py

# Build the Bento service
RUN bentoml build

# Change back to /app directory
#WORKDIR /app
# Run supervisord
#CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
# Run the BentoML service when the container launches
CMD ["bentoml", "serve", "cnn_keras_model_service:latest", "--timeout", "600"]