import os, requests
from http.client import responses


def login(requests):
    auth = requests.authorization
    if not auth:
        return None, ("Missing credentials", 302)

    basicAuth = (auth.username, auth.password)
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_HOST')}/login",
        auth=basicAuth
    )

    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (responses.txt, response.status_code)

