# Upgrade to latest version
apt-get -y update
apt-get -y upgrade
apt-get -y update
apt-get -y upgrade

# Install all dependencies
apt-get -y install python3 python3-pip
pip3 install -r ./requirements.txt

# Create directories
cd ./handwriter_test

mkdir ./handwriter_test/media
mkdir ./handwriter_test/media/AllHandwritings
mkdir ./handwriter_test/media/text_files

# Run collectstatic command
# python3 ./manage.py collectstatic

# Creates database tables
python3 ./manage.py makemigrations
python3 ./manage.py migrate
