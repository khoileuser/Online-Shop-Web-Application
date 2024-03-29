# Online-Web-Application

## Live Demo
Try out live demo <a href="https://shophub.k-cf.cloud/" target="_blank">here</a>

You can use already made test accounts, however **Sign up** is also available

```
Username: testcustomer
Password: testcustomerA1!
```

```
Username: testvendor
Password: testvendorA1!
```

```
Username: testshipper
Password: testshipperA1!
```

## Requirements
- Python >= 3.10
- Django 4

## Installation
0. Clone repo
```bash
git clone https://github.com/khoileuser/Online-Shop-Web-Application
```
1. Virtual environment
- Windows
```bash
python -m venv venv && venv\Scripts\activate
```
- Linux/Mac
```bash
python -m venv venv ; source venv/bin/activate
```

2. Install requirements
```bash
pip install -r requirements.txt
```

3. Load dumped data
```bash
python manage.py migrate
```
```bash
python manage.py loaddata datadump.json
```

4. Run server
```bash
python manage.py runserver
```

## Production
To run website on production version (with `DEBUG=False`)
1. Change git branch
```bash
git checkout production
```

2. Run server
```bash
python manage.py runserver --insecure
```

3. Listen (run on 0.0.0.0)
```bash
python manage.py runserver 0.0.0.0:80 --insecure
```

## Use PostgreSQL as database
1. Create `.env` at root directory with these variables as example
```bash
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="somesupersecretpassword"
POSTGRES_HOST="192.168.2.82"
POSTGRES_PORT="5432"
```
2. Change this part in `shop_web/settings.py` from
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'remote': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': getenv("POSTGRES_USER"),
        'PASSWORD': getenv("POSTGRES_PASSWORD"),
        'HOST': getenv("POSTGRES_HOST"),
        'PORT': getenv("POSTGRES_PORT")
    }
}
```
to
```python
DATABASES = {
    'local': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': getenv("POSTGRES_USER"),
        'PASSWORD': getenv("POSTGRES_PASSWORD"),
        'HOST': getenv("POSTGRES_HOST"),
        'PORT': getenv("POSTGRES_PORT")
    }
}
```
3. Load dumped data
```bash
python manage.py migrate
```
```bash
python manage.py loaddata datadump.json
```

## References
- (2024) The web framework for perfectionists with deadlines | Django, Django Project website, accessed 16 January 2024. https://www.djangoproject.com/
- (2024) Psycopg – PostgreSQL database adapter for Python — Psycopg 2.9.9 documentation, accessed 16 January 2024. https://www.psycopg.org/docs/index.html
- theskumar (2024) GitHub - theskumar/python-dotenv: Reads key-value pairs from a .env file and can set them as environment variables. It helps in developing applications following the 12-factor principles., GitHub website, accessed 16 January 2024. https://github.com/theskumar/python-dotenv
- seatgeek (2024) GitHub - seatgeek/thefuzz: Fuzzy String Matching in Python, GitHub website, accessed 16 January 2024. https://github.com/seatgeek/thefuzz
- adamchainz (2024) GitHub - adamchainz/django-minify-html: Use minify-html, the extremely fast HTML + JS + CSS minifier, with Django., GitHub website, accessed 16 January 2024. https://github.com/adamchainz/django-minify-html