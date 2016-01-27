# Wanderlust API
[![Build Status](https://magnum.travis-ci.com/SCCapstone/wandrlust_api.svg?token=3yQ6ZdxTSiqPugjpthWC&branch=master)](https://magnum.travis-ci.com/SCCapstone/wandrlust_api)

## To run the server locally:
* Clone the repository: `git clone https://github.com/SCCapstone/wandrlust_api.git`
* Create a new virtualenv: `virtualenv venv`
* Source the new venv: `source venv/bin/activate`
* Install all of the required apps: `pip install -r requirements.txt`
* Migrate the database: `python manage.py migrate`
* Create a new super user: `python manage.py createsuperuser`
* Run the server: `python manage.py runserver`

#Make sure to change DEBUG=False in defaults.py for production
