# Porter
A tiny tool that aims to support software development process.

# Setup
1. Clone this repo
2. Install dependencies with ```pip install -r requirements.txt```
3. Make migrations ```./manage.py makemigrations core```
4. Run migrations with ```./manage.py migrate```
   - optionally run ```./manage.py loaddata initial_data``` to populate database with some seed data
5. Start application with ```./manage.py runserver```

# Tests
Tests are located in its corresponding module package. Run tests with ```./manage.py test```
Data for test database is stored in fixture 'test_fixture.json'.
