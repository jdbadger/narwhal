# Introduction

Narwhal is my personal containerized Django starter project template. It's meant to be relatively barebones, but includes some useful default configuration to provide a head start on any new Django project.

Narwhal provides a containerized web application based on Docker with multiple services orchestrated by Docker Compose. Services include:

- A **Caddy** server (automatic HTTPS/TLS!) to manage traffic, with a reverse proxy to Django. The server is configured per environment via caddyfiles. It's a relatively basic config. Customize it according to project requirements (https://caddyserver.com/docs/).

- A **Redis** instance serving as both a cache backend and task queue (https://hub.docker.com/_/redis).

- A **PostgreSQL** database for development (https://hub.docker.com/_/postgres).

- A task runner implemented with the help of the excellent **Huey** library (https://huey.readthedocs.io/en/latest/).

- And of course a **Django** application with:

  - Compressed static files served via **WhiteNoise** with support for brotli compression (https://whitenoise.readthedocs.io/en/latest/).

  - A storages configuration ready to connect to your AWS S3 buckets with the help of the excellent **django-storages** library (https://django-storages.readthedocs.io/en/latest/).

  - **Django Debug Toolbar** for debugging in development (https://django-debug-toolbar.readthedocs.io/en/latest/).

  - A custom user model supporting authentication by email address.

  - For development, a default superuser and password.

Narwhal **_does not_** provide an environment/secrets management solution. If you use this template, environment/secrets management is your responsibility.

# Dev Setup

- Fork this repo!

- Navigate to the project root.

- Create a new .env file using `.env.example`.

  ```
  $ cp .env.example ./docker/.env
  ```

- Make any additions and changes to your .env file and caddy/srv templates according to your project requirements.

  - `USER` (`$ whoami`) and `UID` (`$ id -u $(whoami)`) in `.env`. It's not necessary to provide any additional configuration to bring up the application, but `USER` and `UID` should be defined at a minimum.

  - `COMPOSE_PROJECT_NAME` in `docker/.env`

  - Add your AWS S3 development bucket credentials to `.env` if you want to use S3 for storages in development.

  - Add or change any other `.env` definitions according to your project requirements.

  - Optionally customize caddyfiles. Need dedicated subdomains for api and client services? Just edit `caddy/Caddyfile*` accordingly.

  - Customize Caddy-served templates in `caddy/srv/`. These include references to `Narwhal`. Change them according to your project requirements.

- Bring up the containers:

```
$ docker-compose up -d --build
```

- In your browser, navigate to `localhost:81` (or the host and port you assigned in `.env`). Here you should see the default Django startup page.

- Navigate to `localhost:81/admin/` for the admin login page. You can log in using the superuser account `super@example.com` and the default password `secret`. **_Note_**: It's a security best practice to change the `/admin/` path to anything other than `/admin/`. There's no better time than now!

- To bring the containers down and remove volumes:

```
$ docker-compose down -v
```

That's it!

Again, this is meant to be a barebones starter template. That's not to say Narwhal won't include more features in the future; but for most purposes this should provide a nice base to build from.
