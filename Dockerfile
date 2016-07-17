FROM django:onbuild

RUN git clone https://github.com/UKS-2015/porter.git
WORKDIR /usr/src/app/porter

EXPOSE 8000
RUN ["python", "manage.py", "runserver", "0.0.0.0:8000"]
