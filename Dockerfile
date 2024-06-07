FROM python:3.11.6

WORKDIR /app

ENV PYTHONUNBUFFERED 1

# RUN set -x && \
# 	apt-get update && \
# 	apt -f install	&& \
# 	apt-get -qy install daphne gunicorn

COPY ./scripts/ ./scripts

COPY ./requirements/base.txt /app/base.txt
COPY ./requirements/production.txt /app/production.txt

RUN pip install -r /app/production.txt


COPY . /app/


# sudo docker build -t django/app:backend .
# sudo docker push django/app:backend


# CHEATSHEET
# EXECUTE INSIDE IN CONTAINER
# > docker exec -t -i [ID] /bin/bash
# > docker exec -it [ID] mysql -u root -p 
# > docker exec -it [ID] psql -U {DB_USER} -d Django
