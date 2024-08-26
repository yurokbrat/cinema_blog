# Cinema Blog 🎬

### Welcome to **Cinema Blog**!
This Django-based application uses Python, Django REST Framework (DRF), and Wagtail CMS to manage movie content, user interactions, and more.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Features 🚀

- **Movie Management:** Add, edit, and manage movies with video uploads and encoding in multiple qualities. 🎥
- **User Interaction:** Support for likes, comments, and a blog section. 💬👍
- **Admin Interface:** Intuitive admin dashboard powered by Wagtail CMS. 🛠️

## Setup 🛠️

### Basic Commands

#### Setting Up Users

- **Superuser Account:** Create with the command:

  ```bash
  $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy kino

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd kino
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd kino
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd kino
celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

## Deployment 🚀

### Running Locally
To run the application locally, use the local.yml Docker Compose configuration. This setup includes Django, PostgreSQL, Redis, Mailpit, and other services necessary for development. To start the application, run:

``` bash
docker-compose -f local.yml up --build
```

This command will build and start the containers defined in local.yml, allowing you to develop and test the application on your local machine.

### Production Deployment

For production, use the production.yml Docker Compose configuration. This setup is optimized for a production environment with services like Traefik for reverse proxy and SSL termination. To deploy in production, run:

```bash
docker-compose -f production.yml up --build
```
Ensure that your production environment is properly configured, including environment variables and volumes.

### Running Tests
To run tests, use the test.yml Docker Compose configuration. This setup is tailored for running tests and includes Django, PostgreSQL, Redis, and Celery services. To execute the test suite, use:

```bash
docker-compose -f test.yml run django_kino_test pytest -n auto --create-db
```
This command will set up the test environment and run your test cases.

For more detailed Docker deployment instructions, refer to the cookiecutter-django Docker documentation. 🌐



See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
=======
