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

### Api Docs
Api docs are available under `/docs` endpoint - Swagger UI.

![Screenshot 2024-01-08 at 17.15.52.png](..%2F..%2F..%2F..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fmz%2Fwl3681r93774jr5dn3869jd40000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_ylR97Y%2FScreenshot%202024-01-08%20at%2017.15.52.png)

### Update db schema
Want to update db schema? Sure! :joy:

1. Update model in `database/models.py`
2. run `make generate-db-migration`

### DB ERD
![Screenshot 2024-01-08 at 16.20.32.png](..%2F..%2F..%2F..%2F..%2FDesktop%2FScreenshot%202024-01-08%20at%2016.20.32.png)

### Testing locally without Medicover access

Under `database/dump` there are .csv files attached which could be mapped to a db rows. Write simple script that will load those after setting up database locally.

### Running `/medicover/notifications` or `/medicover/appointments` endpoints

For running those endpoints make sure that you have medicover access. On top of that - for notifications endpoint make sure to set admin_user and admin_password global variables.

Note - this can be done using:

```
export admin_user=Inowrocławska
export admin_password=Bajo_jajo
```