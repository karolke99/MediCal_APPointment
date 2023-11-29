### Setting up db
```
make set-db
```
Prerequisites - make sure that docker is installed + running, you have psql installed and port 5432 is free (you can check that by running `sudo lsof -i :5432`)

This pulls postgres docker container and runs it

If you want to play with psql instance (Note - this connects to db from local machine (not from docker container) - so make sure you have psql installed. You can also run docker container and ping db straight from container itself - docker exec bajo jajo):
```
psql -h localhost -p 5432 -U postgres
```
When prompted for password - use mysecretpassword

### Setting up env
Prerequisites - install pipenv using `pip install pipenv`
```
pipenv --python 3.11
pipenv install
pipenv shell
```

### Running server locally
First setup database tables - `make generate-db-migration`
```
pipenv run gunicorn --worker-tmp-dir /tmp --log-level=DEBUG app:app
```

### Update db schema
Want to update db schema? Sure! :joy:

1. Update model in `database/models.py`
2. run `make generate-db-migration`

Ready to go? Try to use /doctor (POST) and /doctors (GET) endpoints! If you didn't screw that, a very distinguished gentleman should appear...