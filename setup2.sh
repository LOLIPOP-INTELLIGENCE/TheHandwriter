# copy nginx config file to correct location; enable config
sudo cp ./hwnginxconf /etc/nginx/sites-available/default
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# move gunicorn config file to correct location

# move service file to correct location
sudo cp ./handwriterd.service /etc/systemd/system/handwriterd.service

# Reload daemon
sudo systemctl daemon-reload
