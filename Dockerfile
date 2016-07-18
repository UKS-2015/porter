FROM django:onbuild
MAINTAINER Tim 4 <https://github.com/UKS-2015>

# Instaling dependencies
# RUN apt-get update && apt-get -y install python3 && apt-get -y install python3-pip && apt-get -y install git

# RUN mkdir /opt/porter
# ADD . /opt/porter

# For testing purposes
RUN git clone -b master https://github.com/UKS-2015/porter.git /opt/porter

ADD .docker/run.sh /usr/local/bin
RUN pip3 install -r /opt/porter/requirements.txt

EXPOSE 8004

# CMD ["sudo", "apt-get", "install", "sqlite3", "libsqlite3-dev"]
# CMD ["/bin/bash", "-e", "/usr/local/bin/run.sh"]
# CMD ["sudo", "apt-get update"]


# CMD ["python3", "/opt/porter/manage.py", "makemigrations", "--noinput"]
CMD ["python3", "/opt/porter/manage.py", "migrate", "--fake-initial"]
CMD ["python3", "/opt/porter/manage.py", "runserver", "0.0.0.0:8004"]