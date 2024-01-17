# Use a base image with Miniconda installed and a specific platform
FROM condaforge/mambaforge
# Use an official Python runtime as a parent image
#FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory in the container
WORKDIR /app
# Creating the 'uploads' directory
RUN mkdir uploads

# Make RUN commands use `bash --login`:
#SHELL ["/bin/bash", "--login", "-c"]

# Copy the Flask app into the container at /app
COPY . /app
COPY environment.yml /app/
# Install any needed packages specified in requirements.txt
#COPY requirements.txt /app/

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Create a Conda environment using the environment.yml file
RUN mamba env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["mamba", "run", "-n", "myenv", "/bin/bash", "-c"]

# Initialize conda in bash config fiiles:
#RUN conda init bash

# List installed packages (for debugging)
#RUN echo "Listing installed packages in 'myenv':" && \
   ## /opt/conda/envs/myenv/bin/mamba list

# Print environment info (for debugging)
#RUN echo "Environment info:" && \
    #/opt/conda/envs/myenv/bin/conda info

# Define environment variable
ENV FLASK_APP=routes.py
#ENV CONDA_DIR=/opt/conda

COPY start.sh /app/
RUN chmod +x /app/start.sh
ENTRYPOINT ["/app/start.sh"]
# Make RUN commands use the new environment:
#ENTRYPOINT ["mamba", "run", "-n", "myenv", "flask",  "run", "--host=0.0.0.0"]
#RUN python -m pip install --upgrade pip
# Install audio libraries
#RUN apt-get update && apt-get install -y gcc libsndfile1-dev libasound-dev libasound2-dev portaudio19-dev libportaudio2 libsndfile-dev libportaudiocpp0 ffmpeg libgstreamer1.0-dev libav-tools && rm -rf /var/lib/apt/lists/*

#RUN pip install -r requirements.txt

# Run the Flask app when the container launches
#CMD ["flask", "run", "--host=0.0.0.0"]
#CMD echo Using Python from myenv: $(which python) && flask run --host=0.0.0.0