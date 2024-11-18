#!/bin/bash

# Navigate to the project directory
cd /var/www/NCDC/ncdc_project || exit

# Stash any local changes before pulling (if necessary)
git stash

# Pull the latest changes from the main branch
git pull origin main

# Activate the virtual environment
source /var/www/NCDC/venv/bin/activate

# Run Django management commands
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# Restart Gunicorn and Nginx services
sudo systemctl restart gunicorn
sudo systemctl restart nginx

