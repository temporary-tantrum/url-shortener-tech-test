"""
    TODO: doc
"""
import os
from contextlib import asynccontextmanager
import asyncio
from urllib.parse import urlparse
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from redis import asyncio as redis

import silly

PORT: int = int(os.getenv("PORT") or 8000)
BASE_URL: str = os.getenv("BASE_URL") or f"http://localhost:{PORT}"
REDIS_URL: str = os.getenv("REDIS_URL") or "redis://localhost:6379"

# parse redis url into a host and port and password (if applicable)
redis_url = urlparse(REDIS_URL)
redis_host = redis_url.hostname
redis_port = redis_url.port
redis_password = redis_url.password

redis_pool = None
application_services = {}

## this is maybe necessary on windows
## asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_redis_connection(redis_pool: redis.ConnectionPool):
    """
    Test that we can connect to Redis.
    We always do this right after boot-up: if we can't connect to Redis,
        it would be better to fail up-front.
    """
    redis_client = await redis.Redis(
        connection_pool=redis_pool)
    await redis_client.set("test", "test")
    test = await redis_client.get("test")
    assert test == "test"

@asynccontextmanager
async def lifespan(_: FastAPI):
    pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)

    await test_redis_connection(pool)
    application_services['redis_pool'] = pool
    yield
    # giant habbo raid july 12th at 10:00pm
    await pool.close()

app = FastAPI(lifespan=lifespan)

def redis_key(id: str) -> str:
    """
    Return the Redis key for a given ID.
    """
    return f"url:{id}"

class ShortenRequest(BaseModel):
    """
    deef dorf
    """
    url: str

class ShortenResponse(BaseModel):
    """
    beef borf
    """
    short_url: str

@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest):
    """
    Given a URL, generate a short version of the URL that can be
    later resolved to the originally specified URL.
    """
    short_id = silly.name(slugify=True)
    redis_client = redis.Redis(connection_pool=redis_pool)
    print("shoretning::::")
    print(request.url)
    await redis_client.set(redis_key(short_id), request.url)
    return {
        "short_url": f"{BASE_URL}/r/{short_id}",
        "short_id": short_id
    }

@app.post("/url/longen")
async def url_longen(request: ShortenRequest):
    """
    Given a URL, generate a long version of the URL that can be
    later resolved to the originally specified URL.
    """
    long_id = silly.sentence(slugify=True)
    redis_client = redis.Redis(connection_pool=redis_pool)
    await redis_client.set(redis_key(long_id), request.url)

    return {
        "long_url": f"{BASE_URL}/r/{long_id}",
        "long_id": long_id
    }

@app.get("/r/{short_url}")
async def url_resolve(short_url: str):
    """
    Return a redirect response for a valid shortened URL string.
    If the short URL is unknown, return an HTTP 404 response.
    """
    # the default response is just a redirect to the base URL
    redis_client = redis.Redis(connection_pool=redis_pool,
                                decode_responses=True)
    redirect_target = await redis_client.get(redis_key(short_url))
    print("redorircotong: :: >")
    print(redirect_target)
    if not redirect_target:
        return RedirectResponse(BASE_URL)
    return RedirectResponse(redirect_target)


@app.get("/")
async def index():
    """
    let's get this party started
    """
    return "Your URL Shortener is running!"
