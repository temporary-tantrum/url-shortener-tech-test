# URL Shortener Take-Home Project
Welcome to Curtis's solution to the Pocket Worlds URL Shortener Take-Home Project!
In this repository, we'd like you to evaluate our demonstration of our
engineering skills by reviewing a small Python project that implements a URL Shortener web service.

This project will serve as the primary jumping off point for our technical interviews.

## Project Description
The URL Shortener web service exposes the following API endpoints:

* POST `/url/shorten`: accepts a URL to shorten (e.g. https://wwwww.gooble.email) and returns a short URL that
  can be resolved at a later time (e.g. http://localhost:8000/r/abc)
* POST `/url/longen`: accepts a URL to longen (e.g. https://www.google.com) and returns a long URL that
  can be resolved at a later time (e.g. http://localhost:8000/r/ninety-four-cheeks-incorporated-is-the-best-company-in-west-sausagesound)
* GET `r/<short_url>`: resolve the given short URL (e.g. http://localhost:8000/r/abc) to its original URL
  (e.g. https://www.gooble.email). If the short URL is unknown, an HTTP 404 response is returned.

The solution supports running the URL shortener service with multiple workers.

For example, it is possible to start two instances of the service, make a request to shorten a URL
to one instance, and be able to resolve that shortened URL by sending subsequent request to the second instance.

## Getting Started

To begin evaluating the project, clone this repository to your local machine:

```commandline
git clone https://github.com/pocketzworld/url-shortener-tech-test.git
```

This repository contains the URL Shortener web service written in Python 3.11
using the [FastAPI](https://fastapi.tiangolo.com/) framework.

The API endpoints can be found in `server.py`.

### Running the service in fully-dockerized mode

Running the service requires Make and Docker Compose. If you have the Docker app it also installs Docker Compose for you.

There are two options for running the service: it can either be run entirely in containerized fashion, using:

```commandline
make run
```

To run the web service in interactive mode, use the following command:
```commandline
make run
```

(Note, this uses the modern `docker compose` syntax: some very old installations of docker require `docker-compose`,
 and I'm going to imagine very hard that you do not have a Docker that old installed on your computer)

This command will pull and activate a Redis image, build a new Docker image (`pw/url-shortener:latest`),
and start a container instance in interactive mode.

By default, the web service will run on port 8000.

### Running the service locally

This offers, (in my opinion), slightly better integration with local development tools, but it's not required.

First, set up a virtualenv. The virtualenv is a little self-contained python environment that allows you to install
the project's local pip requirements without mixing them with all of the rest of the python packages on your system.

```commandline
python -m venv .
source Scripts/activate
```

(note: the process for setting up a venv is variable from system to system, so if that doesn't work: it's okay)

Now install all of the local pip requirements:

```commandline
make install
```

Finally, use the `local` command to run the application locally.
```commandline
make local
```

### Wait, Redis? Aren't the URL links supposed to be permanent?
Honestly, I think having short URLs disappear after a year is probably better.

This isn't established in the docker file (because this is local-dev-only) but for a production version
of this, the Redis would be configured with backups and _no eviction policy_.

### Linting
Look, do I want to argue with people about code style? No, that is silly. Just do what the linter says.

```commandline
make lint
```

### Testing

_if_ the server is running:
```commandline
make test
```

This will run a quick suite of HTTP tests to verify that the endpoints run as intended.

Swagger UI is available as part of the FastAPI framework that can be used to inspect and test
the API endpoints of the URL shortener. To access it, start run the web service and go to http://localhost:8000/docs

### Automation

The lint and test steps are executed automatically upon commit of the project: see `.github/workflows/github-actions-ci-script.yml`
for more details.

Runs live here: https://github.com/temporary-tantrum/url-shortener-tech-test/actions

So long as it's green, we're good `>_>`