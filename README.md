# URL Shortener Take-Home Project
Welcome to the Pocket Worlds URL Shortener Take-Home Project! In this repository, we'd like you to demonstrate your
engineering skills by creating a small Python project that implements a URL Shortener web service.

This project will serve as the primary jumping off point for our technical interviews.

## Project Description
Using the provided Python project template, your task is to implement a URL Shortener web service that exposes
the following API endpoints:

* POST `/url/shorten`: accepts a URL to shorten (e.g. https://www.google.com) and returns a short URL that 
  can be resolved at a later time (e.g. http://localhost:8000/abc)
* GET `r/<short_url>`: resolve the given short URL (e.g. http://localhost:8000/abc) to its original URL
  (e.g. https://www.google.com). If the short URL is unknown, an HTTP 404 response is returned.

Your solution must support running the URL shortener service with multiple workers.

For example, it should be possible  to start two instances of the service, make a request for to shorten a URL
to one instance, and be able to resolve that shortened URL by sending subsequent request to the second instance. 

## Getting Started

To begin the project, clone this repository to your local machine:

```commandline
git clone https://github.com/pocketzworld/url-shortener-tech-test.git
```

This repository contains a skeleton of the URL Shortener web service written in Python 3.11
using the [FastAPI](https://fastapi.tiangolo.com/) framework.

The API endpoints can be found in `server.py`.

A Makefile and Dockerfile are also included for your convenience to run and test the web service.

You are not required to use Docker for your implementation, so feel free to modify this project and README
to reflect how your implementation should be run and tested.

### Running the service

To run the web service in interactive mode, use the following command:
```commandline
make run
```

This command will build a new Docker image (`pw/url-shortener:latest`) and start a container
instance in interactive mode.

By default, the web service will run on port 8000.

### Testing

Swagger UI is available as part of the FastAPI framework that can be used to inspect and test
the API endpoints of the URL shortener. To access it, start run the web service and go to http://localhost:8000/docs

## Submission Guidelines
When you have completed the project, please follow these guidelines for submission:

1. Commit and push your code to your GitHub repository.
2. Update this README with any additional instructions, notes, or explanations regarding your implementation, if necessary.
3. Provide clear instructions on how to run and test your project.
4. Share the repository URL with the hiring team or interviewer.

## Additional Information
Feel free to be creative in how you approach this project. Your solution will be evaluated based on code quality,
efficiency, and how well it meets the specified requirements. Be prepared to discuss the reasoning behind your
implementation decisions and their trade-offs.

Good luck, and we look forward to seeing your URL Shortener project! If you have any questions or need
clarifications, please reach out to us.
