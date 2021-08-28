# copy nginx config file to correct location; enable config
sudo cp ./hwnginxconf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/ /etc/nginx/sites-available/hwnginxconfig /etc/nginx/sites-available/ /etc/nginx/sites-enabled/hwnginxconfig

# move gunicorn config file to correct location

# move service file to correct location
sudo cp ./handwriterd.service /etc/systemd/system/handwriterd.service

# Reload daemons and start service
sudo systemctl daemon-reload
sudo systemctl start handwriterd
