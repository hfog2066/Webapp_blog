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

 <p>Edit PostgreSQL Database settings.py</p>
 <pre>
 <code>
 DATABASES = {<br />
    'default': {{<br />
        'ENGINE': 'django.db.backends.postgresql_psycopg2',<br />
        'NAME': '<database_name>',<br />
        'USER': '<username>',<br />
        'PASSWORD': '<password>',<br />
        'HOST': 'localhost',<br />
        'PORT': '5432',<br />
    }<br />
 }<br />
 </code>
 </pre>

 Database migrations
 
 blog $ python manage.py makemigrations
 blog $ python manage.py migrate

 Run project

 blog $ python manage.py runserver
 
