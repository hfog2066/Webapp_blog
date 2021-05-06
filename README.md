# This repository contains Web App Blog created with Python3, Django, PostgreSqL 


 <p>Set up</p><br />
 <p>Create folder project</p>
 <pre><code>$ mkdir blog</code><br /></pre>
 <p>Create virtual environment:</p>
 <pre><code>pip install virtualenv</code><br /></pre>
 <pre><code>$ cd blog</code><br /></pre>
 <pre><code>$ virtualenv env</code><br /></pre>
 <pre><code>$ . env/bin/activate</code><br /></pre>
 
 <p>Install Django</p>
 <pre><code>(env)$ django-admin startproject blog</code><br /></pre>
 <pre><code>$ cd blog</code><br /></pre>

 <p>Edit PostgreSQL Database settings.py:</p>
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

 <p>Database migrations</p><br>
 
 <pre><code>blog $ python manage.py makemigrations<br /></code><br /></pre>
 <pre><code>blog $ python manage.py migrate<br /></code><br /></pre>

 <p>Run project<p><br>

 <pre><code>blog $ python manage.py runserver<br /></code><br /></pre>
 
