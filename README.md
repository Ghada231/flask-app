I created a Flask app and implemented task management with CRUD functionality.
I set up PostgreSQL as the database and connected it using SQLAlchemy.
I used Flask-Migrate to handle schema updates and migrations.
I wrote a Dockerfile to containerize the Flask app and set up a docker-compose.yml file to orchestrate the app and database.
I ran the application using docker-compose up and tested the API endpoints.
I ensured the app was portable and ready for deployment in a Dockerized environment.


How to run it :

in Vscode Terminal , run the command line : 
    docker-compose up
    flask --app app.py --debug