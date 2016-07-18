python3 /opt/porter/manage.py flush <<< "yes"
python3 /opt/porter/manage.py makemigrations
python3 /opt/porter/manage.py migrate
python3 /opt/porter/manage.py loaddata initial_data.json
python3 /opt/porter/manage.py runserver 0.0.0.0:8004