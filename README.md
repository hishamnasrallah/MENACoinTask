# MENACoin Evaluation Task



## Development

To start development on this repo or run it, follow these steps:

##### 1. Clone this project
git clone https://github.com/hishamnasrallah/MENACoinTask.git

##### 2. Create and Activate the virtualenv
> The virutalenv is built with __Python 3.7.9__
```
virtualenv venv
venv/bin/activate
```
##### 3. Install Dependencies
> While you are in the virutalenv.
```
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

##### 4. create postgres database
```
CREATE DATABASE menacoin_task_db;
``` 
##### 5. Do database migration
```
python manage.py migrate
# or
python3 manage.py migrate
```

##### 6. Initial fixtures
```
python manage.py loaddata misc/fixtures/*
# or
python3 manage.py loaddata misc/fixtures/* 
```


##### 7. start celery beat
```
celery -A menacoin_task beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

##### 8. start celery worker
```
# Locally (inside your venv)
# windows
celery -A menacoin_task worker --pool=solo -l info
# linux
celery -A menacoin_task worker --loglevel=info
```

##### 9. Run the app
```
python manage.py runserver
# or
python3 manage.py runserver
# Starting development server at http://127.0.0.1:8000/
```

##### 10. create superuser
```
python manage.py createsuperuser
```

##### 11. create api key from django admin 

##### 12. add the task to periodic tasks using django admin or by send put request to the api as following body
```
{"interval": {"every":11, "period": "seconds"}, "task_name": "check_exchange_rate"}
# you can change "every" and "period" but keep the "task_name" value as is.
 
```

###### API REQUEST EXAMPLES ########
```
# add schedule for the task 
curl --location --request PUT 'http://127.0.0.1:8000/api/v1/price/' \
--header 'Authorization: Api-Key 6uPX6al4.fJwnACLd5wIpXSgWDtlnZS61MwPGkBQA' \
--header 'Content-Type: application/json'\
--data-raw '{"interval": {"every":11, "period": "seconds"}, "task_name": "check_exchange_rate"}'

# "get" request  example
it return the current price from alphavantage without storing data in database

curl --location --request GET 'http://127.0.0.1:8000/api/v1/price/' \
--header 'Authorization: Api-Key 6uPX6al4.fJwnACLd5wIpXSgWDtlnZS61MwPGkBQA' \
--data-raw ''

# "post" request example 
it returns the current price from alphavantage with storing it to database (force run task)

curl --location --request POST 'http://127.0.0.1:8000/api/v1/price/' \
--header 'Authorization: Api-Key 6uPX6al4.fJwnACLd5wIpXSgWDtlnZS61MwPGkBQA' \
--data-raw ''


```
