# Wanderlust API
## To run the server locally:
* Clone the repository: `git clone https://github.com/c0cky/wandrlustAPI.git`
* Create a new virtualenv: `virtualenv venv`
* Install all of the required apps: `pip install -r requirements.txt`
* Migrate the database: `python manage.py migrate`
* Create a new super user: `python manage.py createsuperuser`
* Run the server: `python manage.py runserver --settings="wandrlustAPI.settings.local`