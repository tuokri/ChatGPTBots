# MIT License
#
# Copyright (c) 2025 Tuomo Kriikkula
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from enum import StrEnum

import aiocache
import redis.asyncio as redis

from chatgpt_proxy.log import logger
from chatgpt_proxy.utils import is_prod_env


# TODO: think about these namespaces and how to split and use them.
class CacheNamespace(StrEnum):
    Database = "db"
    App = "app"


_default_cache = "redis" if is_prod_env else "memory"
_cache_method = os.getenv("CHATGPT_PROXY_CACHE_METHOD", _default_cache).lower().strip()


def setup_memory_cache(namespace: CacheNamespace) -> aiocache.SimpleMemoryCache:
    return aiocache.SimpleMemoryCache(
        namespace=namespace,
    )


def setup_redis_cache(namespace: CacheNamespace) -> aiocache.RedisCache:
    redis_url = os.environ["REDIS_URL"]
    redis_client = redis.Redis.from_url(redis_url)
    return aiocache.RedisCache(
        redis_client,
        namespace=namespace,
    )


db_cache: aiocache.BaseCache
app_cache: aiocache.BaseCache


def setup_cache(namespace: CacheNamespace) -> aiocache.BaseCache:
    global _cache_method

    if _cache_method == "redis":
        if "REDIS_URL" not in os.environ and not is_prod_env:
            logger.warning(
                f"requested {namespace} cache method is 'redis', but no REDIS_URL is set, "
                f"falling back to in-memory cache (is_prod_env={is_prod_env})"
            )
            cache = setup_memory_cache(namespace)
        else:
            cache = setup_redis_cache(namespace)
        pass  # TODO
    elif _cache_method == "memory":
        cache = setup_memory_cache(namespace)
        pass  # TODO
    else:
        logger.error("invalid cache method: '{}', defaulting to memory")
        _cache_method = "memory"
        cache = setup_memory_cache(namespace)
    return cache


db_cache = setup_cache(CacheNamespace.Database)
app_cache = setup_cache(CacheNamespace.App)

# NOTE: this does not work here, so instead we'll close the cache when
# the Sanic application exits.
# asyncio_atexit.register(cache.close)
