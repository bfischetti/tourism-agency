# Tourism Agency


##To run the project

Install: python3 and pip

In the base of the project: 
```
pip install -e .
py app.py runserver
python3 app.py runserver
```




## If there are changes to the DB model

From the project:

```
flask db migrate
flask db upgrade
```

After deploy to Heroku:
```
heroku login
heroku run flask db upgrade -a fontenay
```

## Test with local server

From the project: 

```
uwsgi --socket 0.0.0.0:8000 --protocol=http -w run:app
```