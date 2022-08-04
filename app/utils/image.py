import base64

import requests
from memoization import cached


@cached(ttl=5, max_size=128)
def load_image_b64(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode("ascii")
