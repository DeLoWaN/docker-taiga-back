# kalumkalac/taiga-back

[Taiga](https://taiga.io/) is a project management platform for startups and agile developers & designers who want a simple, beautiful tool that makes work truly enjoyable.

This Docker image can be used for running the Taiga backend. It works together with the [kalumkalac/taiga-front-dist](https://registry.hub.docker.com/u/kalumkalac/taiga-front-dist/) image.

This image is based on the work of [htdvisser](https://github.com/htdvisser/taiga-docker)

## Running

A [postgres](https://registry.hub.docker.com/_/postgres/) container should be linked to the taiga-back container. The taiga-back container will use the ``POSTGRES_USER`` and ``POSTGRES_PASSWORD`` environment variables that are supplied to the postgres container.

```
docker run --name taiga_back_container_name --link postgres_container_name:postgres kalumkalac/taiga-back
```

## Docker-compose

For a complete taiga installation (``kalumkalac/taiga-back`` and ``kalumkalac/taiga-front-dist``) you can use this docker-compose configuration:

```
data:
  image: tianon/true
  volumes:
    - /var/lib/postgresql/data
    - /usr/local/taiga/media
    - /usr/local/taiga/static
    - /usr/local/taiga/logs
db:
  image: postgres
  environment:
    POSTGRES_USER: taiga
    POSTGRES_PASSWORD: password
  volumes_from:
    - data
taigaback:
  image: kalumkalac/taiga-back:stable
  hostname: dev.example.com
  environment:
    SECRET_KEY: examplesecretkey
    EMAIL_USE_TLS: True
    EMAIL_HOST: smtp.gmail.com
    EMAIL_PORT: 587
    EMAIL_HOST_USER: youremail@gmail.com
    EMAIL_HOST_PASSWORD: yourpassword
  links:
    - db:postgres
  volumes_from:
    - data
taigafront:
  image: kalumkalac/taiga-front-dist:stable
  hostname: dev.example.com
  links:
    - taigaback
  volumes_from:
    - data
  ports:
    - 0.0.0.0:80:80
```

## Environment

* ``SECRET_KEY`` defaults to ``"insecurekey"``, but you might want to change this.
* ``DEBUG`` defaults to ``False``
* ``TEMPLATE_DEBUG`` defaults to ``False``
* ``PUBLIC_REGISTER_ENABLED`` defaults to ``True``

URLs for static files and media files from taiga-back:

* ``MEDIA_URL`` defaults to ``"http://$HOSTNAME/media/"``
* ``STATIC_URL`` defaults to ``"http://$HOSTNAME/static/"``

Domain configuration:

* ``API_SCHEME`` defaults to ``"http"``. Use ``https`` if ``kalumkalac/taiga-front-dist`` is used and SSL enabled.
* ``API_DOMAIN`` defaults to ``"$HOSTNAME"``
* ``FRONT_SCHEME`` defaults to ``"http"``. Use ``https`` if ``kalumkalac/taiga-front-dist`` is used and SSL enabled.
* ``FRONT_DOMAIN`` defaults to ``"$HOSTNAME"``

Email configuration:

* ``EMAIL_USE_TLS`` defaults to ``False``
* ``EMAIL_HOST`` defaults to ``"localhost"``
* ``EMAIL_PORT`` defaults to ``"25"``
* ``EMAIL_HOST_USER`` defaults to ``""``
* ``EMAIL_HOST_PASSWORD`` defaults to ``""``
* ``DEFAULT_FROM_EMAIL`` defaults to ``"no-reply@example.com"``

Database configuration:

* ``POSTGRES_DB_NAME``. Use to override database name.
* ``POSTGRES_USER``. Use to override user specified in linked postgres container.
* ``POSTGRES_PASSWORD``. Use to override password specified in linked postgres container.

## Backup Taiga

Backup database:

```
docker exec -ti taiga_db_container su postgres -c "pg_dump -U taiga -c taiga" > taiga_dump.sql
```

Backup static files:

```
docker run --rm --volumes-from taiga_data_container alpine tar -c /usr/local/taiga/media /usr/local/taiga/static /usr/local/taiga/logs | gzip > taiga_data.tar.gz
```

## Restore Taiga

Restore database:

```
docker exec -ti taiga_db_container su postgres -c "psql -c 'drop database taiga'"
docker exec -ti taiga_db_container su postgres -c "psql -c 'create database taiga'"
docker exec -i taiga_db_container su postgres -c "psql -U taiga taiga" < test_dump.sql
```

Restore static files:

```
docker run --rm --volumes-from taia_data_container -v /path/to/taiga_data.tar.gz:/taiga_data.tar.gz alpine tar xzf /taiga_data.tar.gz
```

## Upgrade Taiga

To upgrade Taiga, proceed [a backup](https://github.com/kalumkalac/docker-taiga-back#backup-taiga) of Taiga.

Stop and remove Taiga containers:

```
docker-compose stop
docker-compose rm
```

Change your docker-compose.yml file to change the version of the images:

```
[...]
taigaback:
  image: kalumkalac/taiga-back:new_version
[...]
taigafront:
  image: kalumkalac/taiga-front-dist:new_version
[...]
```

Up the containers:

```
docker-compose up
```

Proceed with [a restore](https://github.com/kalumkalac/docker-taiga-back#restore-taiga).

Apply the upgrade steps from [Taiga support page](http://taigaio.github.io/taiga-doc/dist/upgrades.html) in the container using docker exec:

```
docker exec -ti taiga_back_container bash
```

DO NOT APPLY THESE STEPS SINCE THEY ARE ALREADY DONE IN THE BUILDING OF THE IMAGE:

```
cd ~/taiga-back
git checkout stable
workon taiga
git pull
```

Proceed directly with these steps:

```
cd /usr/local/taiga/taiga-back
pip install --upgrade -r requirements.txt
```

Restart containers:

```
docker-compose restart
```
