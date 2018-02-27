In your local branch, put reevaluations.db in ~/evaluatethis/django_code (but don’t add the db to the master branch b/c privacy)

Within ~/evaluatethis/django_code:

├── reevaluations.db
├── db.sqlite3
├── manage.py: Django’s command-line utility for administrative tasks. Don't need to edit.
├── find_courses.py: Similar to pa3, this code takes in the inputs from the website and applies them to reevaluations.db.
├── ui
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── search
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py: need to change but idk how yet
|   └── templates
|       |-- index.html: html code for the website's interface
└── static: houses static files like images, JavaScript, and CSS. If we decide to generate all the graphs beforehand, we should store them here https://docs.djangoproject.com/en/2.0/howto/static-files/
|       |-- main.css: css code for the website's interface

To run the code: python3 manage.py runserver