"""
    This is the main entrypoint for the URL shortening service.

    For more information, consult the README.md file, or your nearest librarian.
"""
import os
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from redis import asyncio as redis
from shortening_service import ShorteningService

# this is a surprise tool that will help us later
URL_REGEX = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}" + \
    "\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

# setup, here, with environment variables (with simple, sane defaults)
PORT: int = int(os.getenv("PORT") or 8000)
# in prod this would be https://shortener.example.com
BASE_URL: str = os.getenv("BASE_URL") or f"http://localhost:{PORT}"
REDIS_URL: str = os.getenv("REDIS_URL") or "redis://localhost:6379"

# behold: a global variable
#  (scare chord plays)
application_services = {}

async def test_redis_connection(redis_pool: redis.ConnectionPool):
    """
    Test that we can connect to Redis.
    We always do this right after boot-up: if we can't connect to Redis,
        it would be better to fail up-front.
    """
    redis_client = await redis.Redis(
        connection_pool=redis_pool)
    # This should have a timeout
    await redis_client.set("test", "test")
    test = await redis_client.get("test")
    assert test == "test"

# TODO: FastAPI has a "Dependency" feature that would probably be better here

async def setup():
    """
    Set up the application.
    """
    redis_pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)

    await test_redis_connection(redis_pool)
    application_services['redis_pool'] = redis_pool

    shortening_service = ShorteningService(redis_pool)
    application_services['shortening_service'] = shortening_service

async def teardown():
    """
    Tear down the application.
    """
    await application_services['redis_pool'].aclose()

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan events are a FastAPI feature that allow us to run code before
        the application starts and after it stops.
    Check https://fastapi.tiangolo.com/advanced/events/ for more info.
    (we abstract this into "setup" and "teardown" for clarity)
    """
    await setup()
    yield
    await teardown()

app = FastAPI(lifespan=lifespan)

class ShortenRequest(BaseModel):
    """
    Request to shorten a URL.
    """
    url: Annotated[str, Query(max_length=1000, regex=URL_REGEX)]

class ShortenResponse(BaseModel):
    """
    Look, calling it a "short url" is kind of a misnomer:
        it's just a short token - it's not the URL unless
        the base URL is prepended to it.
    Leaving the name as-is because I don't want to change
        the contract implied by the challenge's original API.
    """
    short_url: str
    short_id: str

class LongenResponse(BaseModel):
    """
    The LongenResponse is different from the ShortenResponse,
        because the longen endpoint returns a long url, not a short one.
    """
    long_url: str
    long_id: str

@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest) -> ShortenResponse:
    """
    Given a URL, generate a short version of the URL that can be
    later resolved to the originally specified URL.
    """
    shortening_service = application_services["shortening_service"]
    short_id = await shortening_service.shorten(request.url)
    return {
        "short_url": f"{BASE_URL}/r/{short_id}",
        "short_id": short_id
    }

@app.post("/url/longen")
async def url_longen(request: ShortenRequest) -> LongenResponse:
    """
    Given a URL, generate a long version of the URL that can be
    later resolved to the originally specified URL.
    """
    shortening_service = application_services["shortening_service"]
    long_id = await shortening_service.longen(request.url)

    return {
        "long_url": f"{BASE_URL}/r/{long_id}",
        "long_id": long_id
    }

@app.get("/r/{short_url}")
async def url_resolve(short_url: str) -> RedirectResponse:
    """
    Return a redirect response for a valid shortened (or longened) URL string.
    If the short URL is unknown, return an HTTP 404 response.
    """
    shortening_service = application_services["shortening_service"]
    redirect_target = await shortening_service.resolve(short_id=short_url)
    return RedirectResponse(redirect_target)


@app.get("/")
async def index():
    """
    let's get this party started
    """
    return "Your URL Shortener is running!"
