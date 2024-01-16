# Online-Web-Application

## Requirements
- Python >= 3.10
- Django 4

## Installation
1. Virtual environment
- Windows
```
python -m venv venv && venv\Scripts\activate
```
- Linux/Mac
```
python -m venv venv ; source venv/bin/activate
```

2. Install requirements
```
pip install -r requirements.txt
```

3. Load dumped data
```
python manage.py migrate
```
```
python manage.py loaddata datadump.json
```

4. Run server
```
python manage.py runserver
```

## Production
To run website on production version (with `DEBUG=False`)
1. Change git branch
```
git checkout production
```

2. Run server
```
python manage.py runserver --insecure
```

3. Listen (run on 0.0.0.0)
```
python manage.py runserver 0.0.0.0:80 --insecure
```

## References
- (2024) The web framework for perfectionists with deadlines | Django, Django Project website, accessed 16 January 2024. https://www.djangoproject.com/
- (2024) Psycopg – PostgreSQL database adapter for Python — Psycopg 2.9.9 documentation, accessed 16 January 2024. https://www.psycopg.org/docs/index.html
- theskumar (2024) GitHub - theskumar/python-dotenv: Reads key-value pairs from a .env file and can set them as environment variables. It helps in developing applications following the 12-factor principles., GitHub website, accessed 16 January 2024. https://github.com/theskumar/python-dotenv
- seatgeek (2024) GitHub - seatgeek/thefuzz: Fuzzy String Matching in Python, GitHub website, accessed 16 January 2024. https://github.com/seatgeek/thefuzz
- adamchainz (2024) GitHub - adamchainz/django-minify-html: Use minify-html, the extremely fast HTML + JS + CSS minifier, with Django., GitHub website, accessed 16 January 2024. https://github.com/adamchainz/django-minify-html