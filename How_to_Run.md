Create a virtual environment inside elevate-backend.
To activate it

`python3 -m venv venv`

`source venv/bin/activate`


Make a .env file in elevate-backend/backend (the same folder as the manage.py file) and add CLIENT_ID

`CLIENT_ID=your-client-id-here`


Install the requirements whenever pulling from the repo to make sure you have all the required libraries 

`pip install -r requirements.txt`


Run migrations whenever you pull from the repo to ensure the changes made in the models are applied to your db

`python manage.py makemigrations`

`python manage.py migrate`


To start the app run 

`python manage.py runserver`

To create a superuser (admin) run 

`python manage.py createsuperuser`

Fill in the details that come up. Go to localhost:8000/admin to access the admin portal

If you have to additionally install any libraries, ACTIVATE THE VIRTUAL ENVIRONMENT and then install the library using

`pip install <package-name>` 

Then in the root directory (the one with the README.md) run

`pip freeze > requirements.txt` 

