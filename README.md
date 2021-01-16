# pokeproject


To install the project just clone the repository, install requeriments.txt and create migrations
if you want you can create the pokemon in database using Celery, just up a redis server in localhost:6379 and run the following commands in diferent consoles

celery -A pokeproject worker -l info

celery -A pokeproject beat -l info


theres two available endpoints 
1 /pokemon/<<pokemon-name>> using GET to retrive a pokemon

2 /pokemon/ using POST to store pokemon in database ONLY IF YOU ARE USING CELERY
payload example


{"name": "<<pokemon name>>"}

if you are no using celery you can use this command to store a pokemon 

python manage.py create_pokemon <<pokemon-name>>

