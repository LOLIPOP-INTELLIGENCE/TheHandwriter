# NAME OF PROJECT = handwriter_main
# NAME OF APP = hwapp

mkdir media/AllHandwritings

# create project, app boilerplate
django-admin startproject $1
cd $1
python3 manage.py startapp $2

# remove boilerplate urls, settings, views
rm --force $1/urls.py
rm --force $1/settings.py
rm --force $2/urls.py
rm --force $2/views.py

# move urls, settings, views to correct locations
ln ../project_dir/urls.py $1/urls.py
ln ../project_dir/settings.py $1/settings.py
ln ../app_dir/urls.py $2/urls.py
ln ../app_dir/views.py $2/views.py
