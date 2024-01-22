## Use a base image with Miniconda installed and a specific platform
FROM condaforge/mambaforge

## Set the working directory in the container
WORKDIR /app
## Creating the 'uploads' directory
RUN mkdir uploads

## Copy the Flask app into the container at /app
COPY . /app
COPY environment.yml /app/
COPY start.sh /app/
RUN chmod +x /app/start.sh

## Make port 5000 available to the world outside this container
EXPOSE 5000

## Create a Conda environment using the environment.yml file
RUN mamba env create -f environment.yml

## Make RUN commands use the new environment:
SHELL ["mamba", "run", "-n", "myenv", "/bin/bash", "-c"]



## Define environment variable
ENV FLASK_APP=routes.py

ENTRYPOINT ["/app/start.sh"]
