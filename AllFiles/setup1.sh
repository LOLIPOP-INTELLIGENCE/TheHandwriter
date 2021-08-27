# create project, app, static, template dirs
django-admin startproject $1
# cd into project dir
cd $1
# create app dir
python3 manage.py startapp $2
# create static, media and templates dir
mkdir static
mkdir media
mkdir templates
