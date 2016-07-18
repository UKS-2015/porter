python3 /opt/porter/manage.py makemigrations core
python3 /opt/porter/manage.py migrate
python3 /opt/porter/manage.py loaddata initial_data.json
python3 /opt/porter/manage.py runserver 0.0.0.0:8004
