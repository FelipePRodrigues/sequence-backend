# Sequence - Backend
##### *version 1.0*

## Requirements
* Python 3.6.9
* Virtual Environments

## How to Run
First, clone the repository:
```shell
$ git clone https://github.com/FelipePRodrigues/sequence-backend.git
```

After, you need to create and activate your virtual enviroment. You can create using Virtualenv (apt install virtualenv):
```shell
$ cd sequence-backend
$ virtualenv env -p python3
$ source env/bin/activate
```

Upgrade pip and setuptools, then install the env requirements:
```shell
$ pip3 install --upgrade pip
$ pip3 install setuptools --upgrade
$ pip3 install -r requirements.txt
```

Install PostgreSQL and create de database:
```shell
$ sudo su
$ apt-get install postgresql-client
$ apt-get install postgresql-12
$ su postgres
$ psql -c "CREATE DATABASE sequence;"
```

Create a *local_settings.py* file inside sequence folder:
```shell
$ touch sequence/local_settings.py
```

Inside the file local_settings.py configure your database, bellow is a template:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'simfaz',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
    }
}

DEBUG =  True
```

Run the migrations:
```shell
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Execute the system:
```shell
$ python3 manage.py runserver 8000
```

## How it Works
The system provides two endpoints:
| Endpoint | Description | Required Parameters (JSON) |
|:--------:|:-----------:|:--------------------------:|
| POST: /api/v1/sequence/| Validates a sequence | letters: string[ ] |
| GET: /api/v1/stats| Returns sequence verification statistics | - |

Some inputs may cause a Bad Request response, below are some examples of invalid inputs:
|Letters Parameter | Response | Response Code |
|:----------------:|:--------:|:-----------:|
|[ ] | This field must not be an empty array. | 400 |
|["BBUU",<br>1234,<br>"BBUU",<br>"BBUU"] | This field must be an array of strings. | 400 |
|["BBUU",<br>"AEHO",<br>"DHDH",<br>"BBUU"] | This field contains invalid letters. | 400 |
|["DUH",<br>"BHD",<br>"DDB"] | This field must represent a square matrix, with at least 4 rows and columns. | 400 |
|["BBUU",<br>"HHDD",<br>"BBUU"] | This field must represent a square matrix, with at least 4 rows and columns. | 400 |