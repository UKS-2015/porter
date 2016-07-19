FROM django:1.9.5
FROM django:onbuild
MAINTAINER Tim 4 <https://github.com/UKS-2015>

RUN git clone -b master https://github.com/UKS-2015/porter.git /opt/porter

ADD .docker/run.sh /usr/local/bin
RUN pip3 install -r /opt/porter/requirements.txt

EXPOSE 8004

CMD ["/bin/bash", "-e", "/usr/local/bin/run.sh"]