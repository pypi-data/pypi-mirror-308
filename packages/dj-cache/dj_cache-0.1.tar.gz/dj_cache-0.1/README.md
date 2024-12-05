# dj-cache

A database-backed eventually consistent Last-Write-Wins cache for Python functions inside a Django application.

## Installation

```sh
pip install \
    git+https://github.com/aalekhpatel07/dj-cache.git#subdirectory=dj-cache
```

## Usage

Example: As a plain decorator on arbitrary functions.

```python
from dj_cache.decorators import cached


@cached(ttl_seconds=10)
def my_expensive_function():
    ...

# The expensive function is only called and waited on once.
# Subsequent calls will be cached and in case the cached value 
# is expired/stale, an update will be triggered in the background 
# without blocking the function call, which will return the last stored value.
# This ensures a Last-Write-Wins cache that is eventually consistent.

# Note: Concurrent calls to update the cache while an update is underway are 
#       ignored.

```

Example: Caching an expensive function used inside a Django view.


```python
# urls.py

import time
from django.urls import path
from django.http import HttpResponse

from dj_cache.decorators import cached


@cached(ttl_seconds=60)
def expensive_function():
    time.sleep(5)
    return 42


def home(request):
    value = expensive_function()
    return HttpResponse(f"Expensive function returned: {value}")


urlpatterns = [
    path("/", home),
]

```
