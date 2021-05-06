# This repository contains Web App Blog created with Python3, Django, PostgreSqL 


 Set up
 Create folder project
 $ mkdir blog
 Create virtual environment
 pip install virtualenv
 $ cd blog
 $ virtualenv env
 $ . env/bin/activate
 
 Install Django
 (env)$ django-admin startproject blog
 $ cd blog

 Edit PostgreSQL Database settings.py
 
 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<database_name>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
 }

 Database migrations
 
 blog $ python manage.py makemigrations
 blog $ python manage.py migrate

 Run project

 blog $ python manage.py runserver
 
