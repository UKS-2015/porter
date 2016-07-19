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

# Contributors
#### [Lazar Nikolić] (https://github.com/theshammy)
- project module (CRUD, add/remove members, assign/unassign roles)
- repository module (CRUD)
- authorization (Auth Mixin) and authentication module (login and registration)
- user profile management
- issue comments
- various view templates
#### [Bojana Zoranović] (https://github.com/BojanaZ)
- issue module (CRUD, all user's issues, change status, add milestone)
- milestone module (CRUD)
- label module (CRUD)
- project layouting
- generic/base templates
- various view templates
