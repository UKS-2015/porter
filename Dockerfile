FROM django:1.9.5
FROM django:onbuild
MAINTAINER Tim 4 <https://github.com/UKS-2015>

RUN git clone -b master https://github.com/UKS-2015/porter.git /opt/porter

RUN pip3 install -r /opt/porter/requirements.txt

EXPOSE 8004

RUN python3 /opt/porter/manage.py makemigrations core
RUN python3 /opt/porter/manage.py migrate
RUN python3 /opt/porter/manage.py loaddata initial_data.json
CMD ["python3", "/opt/porter/manage.py", "runserver", "0.0.0.0:8004"]