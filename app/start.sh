#!/bin/bash
source /opt/conda/etc/profile.d/conda.sh
conda activate myenv
## Start the uWSGI server using the uwsgi.ini configuration
uwsgi --ini /app/uwsgi.ini
##flask run --host=0.0.0.0