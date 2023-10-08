"""
The ShorteningService class is responsible for shortening and longening URLs.
"""

import secrets # safe with me
from typing import Callable
from redis import asyncio as redis
import silly
from fastapi import HTTPException

ONE_YEAR_IN_SECONDS = 60 * 60 * 24 * 365
MAX_TOKEN_RETRIES = 20
KEY_LENGTH = 4

class ShorteningService:
    """
    Mama's little baby loves shortenin', shortenin'
    """

    def __init__(self, redis_pool: redis.ConnectionPool):
        self.redis_pool = redis_pool

    def client(self) -> redis.Redis:
        """
        Return a Redis client.

        (hey, if we were building this into a bigger application,
            this function wouldn't live here)
        """
        return redis.Redis(
            connection_pool=self.redis_pool,
            decode_responses=True)

    @staticmethod
    def redis_key(short_id: str) -> str:
        """
        Return the Redis key for a given short id.
        (in an application that uses any _other_ redis keys, users
            could generate intentional collisions to probe around
            in the Redis database, which a prefix prevents)
        """
        return f"url:{short_id}"

    async def find_and_set_valid_id(self, url, name_function: Callable) -> str:
        """
        Despite the large inherent keyspace of silly, it's possible that
            we'll generate a duplicate ID. This function will keep
            generating IDs until it finds one that doesn't exist in Redis.
        """
        counter = 0
        while counter < MAX_TOKEN_RETRIES:
            counter += 1
            generated_id = name_function()
            response = await self.client().set(
                ShorteningService.redis_key(generated_id),
                url,
                nx=True,
                ex=ONE_YEAR_IN_SECONDS)
            if response:
                return generated_id
        raise HTTPException(status_code=500, detail="Unable to find a valid ID!")

    async def shorten(self, url: str) -> str:
        """
        Shorten a URL.
        """
        def short_token_generator() -> str:
            # if this is getting randomness from where I think it's
            #   getting randomness, this call should be async, right?
            #   dev/urandom is a blocking call, right?
            #   i'm going to leave it as-is for now, tho:
            #   I'm not going to rewrite the random number generator
            #
            #   yet
            return secrets.token_urlsafe(KEY_LENGTH)
        return await self.find_and_set_valid_id(url, short_token_generator)

    async def longen(self, url: str) -> str:
        """
        Longen a URL.
        """
        def long_token_generator() -> str:
            return silly.sentence(slugify=True)
        return await self.find_and_set_valid_id(url, long_token_generator)

    async def resolve(self, short_id: str) -> str:
        """
        Resolve a short URL to its original URL.
        """
        key = ShorteningService.redis_key(short_id)
        redirect_target = await self.client().get(key)
        if not redirect_target:
            raise HTTPException(status_code=404, detail="No such URL!")
        return redirect_target
