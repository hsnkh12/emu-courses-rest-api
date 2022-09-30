# EMU courses Rest API
It's an ongoing Rest API backend for a website i am working on. 
It's built for EMU students to help each other, students can add resources to a specific course, and other students 
can visit and check those resources to make it easy for them to study.

## Features
- Authentiaction system (Login/Logout/Register)
- Filtering and searching for EMU courses
- Get course details 
- Filtering and ordering resrouces
- Add, update and delete resources
- Like and dislike resources 
- Fully functional admin panel

## Tech
- Python
- Django
- Django Rest framework
- PostgreSQL


## Installation

Clone git repo.
```
 git clone https://github.com/hsnkh12/emu-courses-rest-api
```
Create your python virtual environment.
```
python3 -m venv env
```
Activate it and install requirements needed.
```
source env/bin/activate
```
```
pip3 install -r requirements.txt
```
Add EMU courses to the database using my scraping script https://github.com/hsnkh12/django-setup-script

Run the server and test the the app.
```
Python3 manage.py runserver
```








